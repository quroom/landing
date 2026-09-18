# Generated manually for build note seed
from django.db import migrations
from django.utils import timezone

BODY_MARKDOWN = """## 화면에서 결제창은 잘 뜨는데, 왜 결제 누락과 중복 충전이 발생할까요?

최근 Codex나 Claude 같은 AI 도구를 사용해 결제 기능을 구현하는 창업자와 개발자가 많습니다. 프론트엔드에서 SDK 자바스크립트를 복사해 넣으면 카드 결제창이나 카카오페이 창이 멋지게 뜨고, 결제 완료 알림창까지 완벽하게 동작합니다.

하지만 실서비스에 배포한 직후 고객 문의가 쏟아지기 시작합니다:

> "카드사에서 5만 원 결제 문자는 왔는데, 사이트에는 구매 내역이 없고 포인트도 안 들어왔어요!"
> "새로고침을 눌렀더니 포인트가 2번 충전되었어요."

이 문제는 AI가 잘못 코딩해서가 아닙니다. **결제 시스템의 분산 트랜잭션(브라우저-결제대행사-백엔드 서버) 특성**을 이해하지 못하고 프론트엔드 콜백에만 의존했기 때문에 발생하는 전형적인 아키텍처 결함입니다.

포트원(PortOne V2)과 토스페이먼츠 연동 시 반드시 구축해야 하는 3대 안전장치를 실전 Django 코드로 정리합니다.

---

## 1. 프론트엔드 결제 콜백만 믿으면 결제 누락이 터지는 이유

일반적인 초보자의 결제 처리 흐름은 다음과 같습니다:

1. 브라우저에서 포트원 SDK 결제창을 띄웁니다.
2. 사용자가 카드를 긁고 인증을 마칩니다.
3. SDK의 `response` 콜백 함수 안에서 백엔드 API(`/api/orders/complete/`)로 `paymentId`를 전송합니다.
4. 백엔드가 DB에 주문을 저장하고 완료 처리합니다.

### 💣 문제점: 3번과 4번 사이의 단절
- 사용자가 카드사 결제 완료 팝업을 본 직후 **브라우저 탭을 바로 닫아버리는 경우**
- 모바일 환경에서 결제 완료 직후 엘리베이터에 타서 **네트워크(LTE/5G)가 끊기는 경우**
- 브라우저 메모리 부족으로 탭이 크래시되는 경우

이 경우 카드사에서는 정상 결제되어 돈이 빠져나갔지만, 브라우저가 내 서버에 완료 요청을 보내지 못해 **DB에는 주문이 영원히 생성되지 않습니다.**

### ✅ 해결책: 포트원 웹훅(Webhook) 필수 수신
클라이언트(브라우저)는 언제든 끊어질 수 있는 불안정한 환경입니다. 따라서 결제 완료의 진실(Single Source of Truth)은 포트원 서버가 내 백엔드 서버로 직접 쏴주는 **웹훅(Webhook)**을 통해 처리해야 합니다.

---

## 2. 결제 금액 위변조 방어 (서버 단건 조회 검증)

악의적인 사용자는 브라우저의 개발자 도구(F12)나 프록시 툴을 이용해 50,000원짜리 결제 요청 파라미터를 **100원**으로 변조하여 결제창을 띄울 수 있습니다.

PG사는 100원이 정상 결제되었으므로 백엔드에 "결제 완료" 신호를 보냅니다. 백엔드가 "결제 성공했네?" 하고 그냥 주문을 열어주면 100원에 5만 원짜리 상품이 출고되는 치명적인 보안 사고가 발생합니다.

### ✅ 해결 절차
웹훅이나 완료 요청을 받았을 때, 반드시 포트원 REST API를 서버에서 직접 호출하여 **실제 카드사에서 결제된 금액**과 **우리 DB의 원래 주문 금액**이 1원도 틀리지 않고 일치하는지 대조해야 합니다.

```python
import os
import requests

PORTONE_API_SECRET = os.getenv("PORTONE_API_SECRET")

def verify_portone_payment(payment_id: str, expected_amount: int) -> bool:
    url = f"https://api.portone.io/payments/{payment_id}"
    headers = {
        "Authorization": f"PortOne {PORTONE_API_SECRET}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code != 200:
        return False

    payment_data = response.json()
    status = payment_data.get("status")
    actual_amount = payment_data.get("amount", {}).get("total")

    # 결제 완료 상태인지, 실제 결제 금액이 우리 주문 금액과 일치하는지 엄격 검증
    if status == "PAID" and actual_amount == expected_amount:
        return True
    return False
```

---

## 3. 웹훅 재전송과 중복 충전을 막는 멱등성(Idempotency) 보장

포트원 웹훅 시스템은 신뢰성을 위해 내 서버가 `HTTP 200 OK`를 리턴할 때까지 일정 주기로 웹훅을 **재전송**합니다:

- 내 서버의 DB 작업이 3초 이상 지연되어 포트원 타임아웃(Timeout)이 발생한 경우
- 네트워크 순단으로 내 서버의 200 응답 패킷이 포트원에 닿지 않은 경우

만약 웹훅 핸들러가 들어올 때마다 포인트를 충전하거나 주문 수량을 깎는다면, 재전송된 요청에 의해 포인트가 2배, 3배로 지급됩니다.

이를 방지하는 핵심 설계가 바로 **멱등성(Idempotency, 연산을 여러 번 적용해도 결과가 달라지지 않는 성질)**입니다.

### ✅ 해결 절차: DB 트랜잭션 락과 상태 머신

1. `payment_id`를 데이터베이스의 유니크 키(`unique=True`)로 설정합니다.
2. `transaction.atomic()`과 `select_for_update()`로 동시 유입되는 중복 요청의 레이스 컨디션을 차단합니다.
3. 주문 상태가 이미 `PAID`라면 아무 작업도 하지 않고 즉시 `HTTP 200 OK`를 반환합니다.

```python
# views.py (Django 결제 웹훅 엔드포인트)
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Order

@csrf_exempt
def portone_webhook_view(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
        payment_id = payload.get("data", {}).get("paymentId")
        if not payment_id:
            return HttpResponse(status=400)
    except Exception:
        return HttpResponse(status=400)

    # DB 트랜잭션 락을 걸고 멱등성 보장 처리
    with transaction.atomic():
        try:
            # 동시 요청이 들어와도 한 번에 하나의 스레드만 주문에 접근
            order = Order.objects.select_for_update().get(payment_id=payment_id)
        except Order.DoesNotExist:
            # 주문 정보가 없으면 404가 아닌 200/400 명확히 반환
            return HttpResponse(status=404)

        # 이미 처리된 결제라면 재충전 없이 즉시 200 반환 (멱등성 보장)
        if order.status == "PAID":
            return HttpResponse("ALREADY_PROCESSED", status=200)

        # 포트원 단건 조회를 통한 금액 검증
        if not verify_portone_payment(payment_id, order.total_amount):
            order.status = "VERIFICATION_FAILED"
            order.save(update_fields=["status"])
            return HttpResponse("AMOUNT_MISMATCH", status=400)

        # 정상 결제 완료 처리
        order.status = "PAID"
        order.paid_at = timezone.now()
        order.save(update_fields=["status", "paid_at"])

    # 포트원 재전송 중단을 위해 반드시 200 OK 응답
    return HttpResponse("SUCCESS", status=200)
```

---

## 📋 결제 연동 실서버 배포 전 1분 체크리스트

- [ ] **웹훅 등록**: 포트원 관리자 콘솔에 실서버 웹훅 URL(`https://mydomain.com/api/payments/webhook/`) 등록 완료
- [ ] **CSRF 제외**: 웹훅 URL에 `@csrf_exempt` 데코레이터를 붙여 외부 POST 요청 차단 방지
- [ ] **금액 대조**: 프론트 전달 금액만 믿지 않고 백엔드에서 포트원 V2 REST API로 실결제금액 전수 대조
- [ ] **멱등성 방어**: 중복 웹훅 수신 시 재충전되지 않도록 `select_for_update()` 및 상태 머신 구축
- [ ] **API Secret 관리**: `PORTONE_API_SECRET`은 Git에 커밋하지 않고 서버 환경변수로 분리

---

### 결제 연동과 정산 아키텍처 점검이 필요하신가요?

화면은 완성했으나 포트원·토스페이먼츠 결제 누락, 웹훅 403 오류, 중복 충전 방지 아키텍처에서 막히셨다면 큐룸(QUROOM)의 **[15분 무료 코드·배포 진단](/free-diagnosis/)**을 신청해 주세요. 8년 차 풀스택 엔지니어가 직접 결제 플로우를 점검하고 안전한 릴리즈 경로를 안내해 드립니다.
"""


def seed_portone_webhook_note(apps, schema_editor):
    BuildNote = apps.get_model("landing", "BuildNote")
    BuildNote.objects.update_or_create(
        slug="portone-v2-webhook-idempotency-guide",
        defaults={
            "title": "포트원 V2 결제 연동과 웹훅 처리: 돈은 빠져나갔는데 주문이 누락되는 원인과 해결법",
            "summary": (
                "Codex나 Claude로 결제창을 띄운 뒤 결제 완료 브라우저를 닫았을 때 발생하는 "
                "주문 누락, 웹훅 재전송 시 중복 충전, 결제 금액 위변조를 막는 "
                "Django 실전 멱등성 아키텍처를 정리합니다."
            ),
            "body_markdown": BODY_MARKDOWN,
            "category": "solo_dev",
            "tags": "포트원,결제연동,웹훅,Django,멱등성,PortOne,결제검증",
            "seo_title": "포트원 V2 결제 웹훅 연동과 중복 결제 방지(멱등성) 가이드",
            "seo_description": (
                "포트원 V2 결제창 연동 시 발생하는 주문 누락 원인, REST API 금액 위변조 검증, "
                "Django 웹훅 멱등성(select_for_update) 처리 완전체 코드 스니펫입니다."
            ),
            "status": "published",
            "published_at": timezone.now(),
        },
    )


def unseed_portone_webhook_note(apps, schema_editor):
    BuildNote = apps.get_model("landing", "BuildNote")
    BuildNote.objects.filter(slug="portone-v2-webhook-idempotency-guide").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0013_seed_vibe_coding_deploy_build_note"),
    ]

    operations = [
        migrations.RunPython(seed_portone_webhook_note, unseed_portone_webhook_note),
    ]
