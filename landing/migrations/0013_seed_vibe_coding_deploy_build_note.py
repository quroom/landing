from django.db import migrations
from django.utils import timezone

BODY_MARKDOWN = """## 로컬에서는 잘 돌았는데, 서버에 올리니 502 에러가 뜹니다

최근 Cursor, Claude Code, Codex 등 AI 도구로 프로토타입이나 MVP를 3~5일 만에 완성하는 사례가 많아졌습니다. 화면(UI)과 로컬 비즈니스 로직은 놀라울 만큼 빠르게 구현되지만, 대다수의 비개발자 창업자나 주니어 개발자가 **실서버(VPS, Cloudtype, AWS, Dokku) 배포 단계**에서 며칠 동안 멈춰 서게 됩니다.

로컬 환경(`localhost:3000`, `127.0.0.1:8000`)과 프로덕션 리눅스 서버 환경 사이에는 **네트워크 바인딩, 마이그레이션 트랜잭션, 비동기 웹훅 보안 검증**이라는 엔지니어링 간극이 존재하기 때문입니다.

8년 차 풀스택 개발사로서 지난 1년간 바이브코딩 코드를 실서버에 안정화하며 가장 빈번하게 마주친 4가지 기술적 장애와 그 해결 절차를 명확한 코드와 함께 공유합니다.

---

### 1. 호스트 바인딩 오류: 왜 컨테이너 외부에서 접속이 안 되는가?

가장 흔한 502 Bad Gateway의 원인은 **호스트 IP 바인딩**입니다.

#### 원인
Next.js나 Node.js, Fastify 서버를 로컬에서 실행하면 기본적으로 `localhost` 또는 `127.0.0.1`로 바인딩됩니다. 하지만 Docker 컨테이너나 리버스 프록시(Nginx) 뒤에서 실행될 때는 `127.0.0.1`로 바인딩할 경우 컨테이너 내부 루프백 인터페이스에만 갇혀 외부 Nginx의 포워딩 요청을 전혀 수신하지 못합니다.

#### 해결 절차
호스트를 반드시 모든 인터페이스인 `0.0.0.0`으로 명시하여 바인딩해야 합니다.

```bash
# Next.js standalone 실행 시 (Dockerfile 또는 Procfile)
HOSTNAME="0.0.0.0" PORT=3000 node server.js

# FastAPI / Uvicorn 실행 시
uvicorn main:app --host 0.0.0.0 --port 8000
```

Nginx 리버스 프록시 설정에서는 upstream을 `127.0.0.1:포트`로 연결하고, 클라이언트의 실제 IP와 HTTPS 프로토콜 정보를 전달하도록 헤더를 누락 없이 포워딩해야 합니다:

```nginx
location / {
    proxy_pass http://127.0.0.1:3000;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

### 2. 데이터베이스 마이그레이션 히스토리 충돌

AI에게 프롬프트로 "이 모델에 컬럼 추가해줘", "이 관계 변경해줘"를 반복 요청하면 마이그레이션 파일 의존성이 꼬여 배포 단계에서 `InconsistentMigrationHistory` 에러가 터집니다.

#### 원인
- 로컬 SQLite DB에는 임의로 컬럼이 반영되어 있는데, 마이그레이션 파일 번호(`0003_...`, `0004_...`)가 분기되거나 누락됨.
- 프로덕션 PostgreSQL에 처음 마이그레이션을 적용할 때 외래키 제약조건(Foreign Key Constraint) 순서가 어긋남.

#### 해결 절차
배포 전 로컬에서 마이그레이션 의존성 트리를 점검하고, 필요한 경우 안전하게 정리해야 합니다:

```bash
# Django 마이그레이션 상태 전수 확인
python manage.py showmigrations

# 의존성이 꼬였을 때는 로컬 DB 백업 후 마이그레이션 스쿼시(Squash)
python manage.py squashmigrations <app_name> <squash_target>

# Prisma / Node.js의 경우
npx prisma migrate status
npx prisma migrate deploy
```

⚠️ **주의**: 개발 환경에서 편하다고 `prisma db push`나 `migrate --fake`로 때우면, 실서버의 프로덕션 데이터가 들어간 이후에는 컬럼 타입 변경 시 테이블 락(Lock)이나 데이터 유실이 발생할 수 있습니다.

---

### 3. 결제 모듈(PortOne / Toss) 웹훅 서버 검증 누락

바이브코딩으로 결제를 붙일 때 90% 이상 발생하는 치명적인 보안 결함입니다.

#### 원인
프론트엔드 자바스크립트의 `onSuccess` 콜백만 믿고 브라우저에서 바로 "결제 완료" API를 호출하여 상품을 지급하도록 코드를 작성하는 경우가 많습니다. 이는 브라우저 개발자 도구의 콘솔이나 네트워크 탭에서 결제 완료 API를 직접 위조 호출하면 0원으로 유료 기능을 열 수 있는 상태를 의미합니다.

#### 해결 절차
반드시 PG사 웹훅(Webhook) 엔드포인트를 서버에 개설하고, 결제 금액과 멱등성(Idempotency)을 백엔드에서 교차 검증해야 합니다.

1. **상태 머신 관리**: 결제 요청 시 DB에 주문 레코드를 `STATUS_READY` 상태로 생성.
2. **웹훅 수신 시 PG사 조회 API 재검증**:
   - 웹훅으로 들어온 `payment_id`로 포트원/토스페이먼츠 서버에 직접 시크릿 키로 결제 내역을 재조회.
   - PG 서버에서 응답받은 실제 결제 금액(`amount`)과 DB의 주문 금액이 일치하는지 비교.
   - 일치할 때만 `STATUS_PAID`로 트랜잭션 업데이트 및 권한 부여.

---

### 4. 환경변수(Build-time vs Runtime) 혼동

Next.js 등 최신 프레임워크에서 환경변수를 다룰 때 흔히 겪는 문제입니다.

#### 원인
`NEXT_PUBLIC_` 접두사가 붙은 환경변수는 **빌드 타임(Docker build 시점)**에 클라이언트 번들 JS 코드 안으로 인라인 하드코딩됩니다. 반면 `DATABASE_URL`이나 `SECRET_KEY` 같은 민감 정보는 **런타임(서버 실행 시점)**에 컨테이너로 주입되어야 합니다.

빌드 시점에 환경변수가 주입되지 않아 프론트엔드 API 호출 주소가 `undefined/api/v1`으로 나가거나, 빌드 자체가 실패하는 현상이 발생합니다.

#### 해결 절차
- 클라이언트에 노출되어도 되는 공개 설정만 `NEXT_PUBLIC_`을 붙이고 빌드 인자(Build Arg)로 넘깁니다.
- DB 비밀번호, 결제 API 시크릿 키는 절대 `NEXT_PUBLIC_`을 붙이지 않고 서버 환경변수로 격리 주입합니다.

---

### 요약 및 체크리스트

1. **호스트 바인딩**: `0.0.0.0`으로 서버 열기 + Nginx 리버스 프록시 헤더 설정
2. **마이그레이션**: 배포 전 `showmigrations` / `migrate status`로 단일 체인 검증
3. **결제 보안**: 브라우저 콜백 대신 백엔드 웹훅 + 금액 교차 검증 필수
4. **환경변수**: 빌드 타임 변수와 런타임 시크릿 분리 주입

---

### 바이브코딩 배포 및 아키텍처 점검이 막히셨나요?

화면은 만들었으나 실서버 배포, DB 마이그레이션 충돌, 결제 연동 검증에서 막히셨다면 큐룸(QUROOM)의 **[15분 무료 코드·배포 진단](/free-diagnosis/)**을 신청해 주세요. 8년 차 풀스택 엔지니어가 직접 코드를 검토하고 실서버 배포 경로를 안내해 드립니다.
"""


def seed_vibe_coding_deploy_note(apps, schema_editor):
    BuildNote = apps.get_model("landing", "BuildNote")
    BuildNote.objects.update_or_create(
        slug="vibe-coding-deploy-troubleshooting",
        defaults={
            "title": "Cursor·Claude 생성 코드를 실서버에 배포할 때 발생하는 기술적 장애 4가지와 해결 절차",
            "summary": (
                "로컬 환경(localhost:3000)에서는 잘 돌던 Cursor, Claude 코드가 "
                "VPS나 클라우드 배포 시 502 에러, 마이그레이션 충돌, 결제 누락으로 멈추는 "
                "4대 원인과 실전 해결 코드 스니펫을 정리합니다."
            ),
            "body_markdown": BODY_MARKDOWN,
            "category": "solo_dev",
            "tags": "바이브코딩,배포에러,Docker,Nginx,Cursor,502BadGateway",
            "seo_title": "Cursor·Claude 생성 코드 실서버 배포 에러 4가지와 해결법",
            "seo_description": (
                "Cursor, Claude 코드를 실서버에 배포할 때 발생하는 502 에러, "
                "호스트 바인딩, DB 마이그레이션 충돌, 결제 웹훅 검증 절차를 정리했습니다."
            ),
            "status": "published",
            "published_at": timezone.now(),
        },
    )


def unseed_vibe_coding_deploy_note(apps, schema_editor):
    BuildNote = apps.get_model("landing", "BuildNote")
    BuildNote.objects.filter(slug="vibe-coding-deploy-troubleshooting").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0012_contactinquiry_ad_creative"),
    ]

    operations = [
        migrations.RunPython(
            seed_vibe_coding_deploy_note, unseed_vibe_coding_deploy_note
        ),
    ]
