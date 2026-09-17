from django.db import migrations
from django.utils import timezone

BODY_MARKDOWN = """## 화면은 3일 만에 만들었는데, 도메인 연결과 서버 배포에서 멈춰 섰습니다

최근 Cursor, Claude Code 등 AI 도구를 활용해 3~5일 만에 웹 서비스나 MVP 프로토타입을 완성하는 분들이 정말 많아졌습니다. 화면(UI)도 깔끔하고 내 컴퓨터(`127.0.0.1:8000`)에서는 결제나 기능이 완벽하게 돌아가니, 금방이라도 서비스를 런칭할 수 있을 것 같은 자신감이 듭니다.

하지만 진짜 싸움은 **도메인을 구매하고 리눅스 서버에 올리는 배포 단계**에서 시작됩니다.

코드를 짜는 것과, 전 세계 인터넷 사용자가 접속할 수 있도록 **도메인(DNS)을 연결하고, 웹서버 포트를 열고, 보안 인증서(HTTPS)를 달고, 백엔드 설정을 프로덕션 모드로 전환하는 것**은 완전히 다른 엔지니어링 영역이기 때문입니다.

8년 차 풀스택 개발사로서 초보 창업자나 비개발자 바이브코더가 가장 흔하게 마주치는 **DNS/인프라 연결 4단계**와 **Django 프레임워크 배포 에러 3가지**를 실전 해결책과 함께 총정리합니다.

---

## Part 1. 도메인 & 인프라 연결: 사이트를 세상에 띄우는 4단계

### 1. 도메인 샀는데 왜 안 뜰까? (DNS A 레코드와 전파 시간)

가비아, 후이즈, 네임칩 등에서 도메인(예: `mydomain.com`)을 구매했지만, 사이트에 접속하면 "사이트에 연결할 수 없음"만 뜹니다.

#### 원인
도메인은 단순한 '주소 이름표'일 뿐입니다. 이 이름표가 내 실제 호스팅 서버(VPS, AWS, 라이트세일)의 **공인 IP 주소**를 가리키도록 연결해 주지 않으면 아무 일도 일어나지 않습니다.

#### 해결 절차
1. 도메인을 구매한 사이트의 **[DNS 레코드 설정]** 메뉴로 들어갑니다.
2. 아래와 같이 **A 레코드 2개**를 추가합니다:
   - **타입**: `A` / **호스트**: `@` (루트 도메인) / **값**: `내 서버 공인 IP`
   - **타입**: `A` / **호스트**: `www` / **값**: `내 서버 공인 IP`
3. ⚠️ **주의**: 저장 후 전 세계 DNS 서버로 이 정보가 퍼져나가는 시간(TTL)이 보통 **10분~30분** 걸립니다. 설정 직후 안 된다고 레코드를 지웠다 다시 쓰지 마시고, 차분히 기다려야 합니다.

---

### 2. 주소 뒤에 `:8000` 안 붙이면 접속이 안 되는 문제 (Nginx 리버스 프록시)

내 컴퓨터에서는 잘 돌던 웹서버를 서버에 올렸더니, 주소창에 `http://mydomain.com:8000`처럼 포트 번호를 붙여야만 들어가지고 그냥 치면 접속이 안 됩니다.

#### 원인
일반 사용자의 웹 브라우저는 주소를 칠 때 기본적으로 **80번(HTTP)** 또는 **443번(HTTPS)** 포트로 문을 두드립니다. 하지만 내 파이썬/Django 프로그램(Gunicorn)은 보통 `8000번`이나 `5000번`에서 돌고 있습니다.

#### 해결 절차
서버 앞단에 **Nginx(엔진엑스)** 웹서버를 세워서, 80번 문으로 들어온 손님을 8000번 방의 Django 프로그램으로 자연스럽게 안내해 주는 **리버스 프록시(Reverse Proxy)**를 구성합니다.

```nginx
# /etc/nginx/sites-available/default 예시
server {
    listen 80;
    server_name mydomain.com www.mydomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;  # 8000번 Django로 전달
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

### 3. 내 컴퓨터(SSH 터미널) 끄면 사이트가 같이 죽는 현상 (데몬 띄우기)

원격 서버에 접속해서 `python manage.py runserver`를 실행해 두었는데, 노트북을 덮거나 SSH 터미널 창을 닫는 순간 웹사이트가 바로 먹통이 됩니다.

#### 원인
터미널 세션에 종속된 포그라운드(Foreground) 프로세스로 서버를 띄웠기 때문입니다. 터미널 창이 닫히면 운영체제가 해당 세션에서 돌던 모든 프로그램을 함께 강제 종료합니다.

#### 해결 절차
터미널이 꺼져도, 서버 컴퓨터가 재부팅되어도 스스로 항상 살아있도록 **백그라운드 데몬(systemd 서비스)**이나 **Docker/Dokku**로 실행해야 합니다.

또한 Gunicorn을 실행할 때는 반드시 외부 요청을 모두 받을 수 있도록 `0.0.0.0`으로 바인딩해야 Nginx와 정상 통신합니다:

```bash
# Gunicorn 백그라운드 실행 또는 Procfile 명령
gunicorn --workers=2 --threads=2 --bind 0.0.0.0:8000 landing.project.wsgi:application
```

---

### 4. '주의 요함 / 안전하지 않은 사이트' 빨간 자물쇠 (HTTPS 적용)

도메인으로 접속은 되는데, 브라우저가 빨간 경고창을 띄우며 위험한 사이트라고 막아서 고객들이 다 도망갑니다.

#### 원인
데이터가 암호화되지 않는 일반 HTTP(80번 포트)로 서비스 중이기 때문입니다. 결제, 로그인, 개인정보를 다루려면 반드시 보안 인증서(SSL)가 설치된 HTTPS(443번 포트)가 필수입니다.

#### 해결 절차
비싼 돈 주고 유료 SSL을 살 필요 없이, 전 세계 표준인 **Let's Encrypt (Certbot)**를 사용하면 명령어 한 줄로 무료 인증서 발급과 자동 갱신까지 끝납니다:

```bash
# Ubuntu/Debian 기준 Nginx용 Certbot 자동 설치
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d mydomain.com -d www.mydomain.com
```

실행 후 이메일을 입력하고 약관에 동의하면, Nginx 설정 파일에 SSL 설정과 HTTP ➡️ HTTPS 자동 이동(301 Redirect)까지 알아서 완료해 줍니다.

---

## Part 2. Django 프레임워크: 배포하자마자 터지는 3대 코드 에러

인프라와 DNS를 연결한 뒤, Django 코드 자체에서 터지는 가장 대표적인 3가지 문제입니다.

### 5. `DEBUG = False` 바꾸는 순간 스타일(CSS/JS) 증발

로컬에서는 예쁘던 사이트가 실서버에 올리고 보안을 위해 `DEBUG = False`로 바꾸는 순간 90년대 텍스트 문서처럼 변하고 모든 CSS/이미지가 `404 Not Found`로 깨집니다.

#### 원인 & 해결
Django 개발 서버는 `DEBUG=True`일 때만 정적 파일을 알아서 서빙합니다. 실서버(`DEBUG=False`)에서는 고속 정적 파일 서빙 라이브러리인 **WhiteNoise**를 사용해야 합니다.

1. **`settings.py` 설정**:
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # SecurityMiddleware 바로 다음 위치
    # ...
]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

2. **배포 시 정적 파일 모으기 실행**:
```bash
python manage.py collectstatic --noinput
```

---

### 6. 도메인 연결하자마자 `400 Bad Request` & `403 CSRF 오류`

도메인을 연결해 접속했더니 하얀 화면에 `Bad Request (400)`만 뜨거나, 문의하기/로그인 폼을 누르면 `CSRF verification failed (403)`가 발생합니다.

#### 원인 & 해결
Django의 철저한 보안 기능 때문입니다. 구매한 도메인을 `settings.py`의 허용 목록에 등록해야만 차단이 풀립니다:

```python
# settings.py
ALLOWED_HOSTS = ["mydomain.com", "www.mydomain.com", "localhost", "127.0.0.1"]

# Django 4.0 이상 필수: HTTPS 프로토콜 포함 도메인 등록
CSRF_TRUSTED_ORIGINS = [
    "https://mydomain.com",
    "https://www.mydomain.com",
]
```

---

### 7. 로컬 SQLite 쓰다가 PostgreSQL 올릴 때 마이그레이션 충돌

로컬에서는 `db.sqlite3` 파일 하나로 아무 문제 없이 동작했는데, 실서버에서 PostgreSQL이나 MySQL을 붙이고 `python manage.py migrate`를 치면 `InconsistentMigrationHistory` 에러가 나며 배포가 멈춥니다.

#### 원인 & 해결
AI에게 프롬프트로 "이 필드 추가해줘", "이 관계 바꿔줘"를 반복 요청하다 보면 로컬 마이그레이션 파일 간의 순서(의존성)가 꼬이게 됩니다.

- 배포 전 `python manage.py showmigrations`로 누락되거나 꼬인 마이그레이션 번호가 없는지 전수 검증합니다.
- 파일이 너무 지저분하게 꼬였다면 로컬에서 `python manage.py squashmigrations <앱이름> <목표번호>`로 단일 체인으로 압축한 뒤 배포합니다.

---

## 📋 실서버 배포 전 1분 최종 점검표

- [ ] **DNS**: 가비아에서 A 레코드에 서버 공인 IP 입력 완료
- [ ] **포트 프록시**: Nginx 리버스 프록시로 80/443 포트를 Django(8000)로 포워딩
- [ ] **프로세스**: SSH 창을 꺼도 안 죽도록 Gunicorn을 데몬(systemd/Docker)으로 구동
- [ ] **HTTPS**: Let's Encrypt Certbot으로 자물쇠 장착
- [ ] **Django 설정**: WhiteNoise 미들웨어 + `collectstatic` + `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` 등록

---

### 도메인 연결과 서버 배포에서 막히셨나요?

화면은 다 만들었으나 도메인 DNS 설정, Nginx 502 에러, HTTPS 인증서 설치, Django 정적 파일 서빙에서 며칠째 멈춰 서 계시다면 큐룸(QUROOM)의 **[15분 무료 코드·배포 진단](/free-diagnosis/)**을 신청해 주세요. 8년 차 풀스택 엔지니어가 직접 원인을 진단하고 실서버 배포 경로를 짚어 드립니다.
"""


def seed_vibe_coding_deploy_note(apps, schema_editor):
    BuildNote = apps.get_model("landing", "BuildNote")
    BuildNote.objects.update_or_create(
        slug="vibe-coding-deploy-troubleshooting",
        defaults={
            "title": "바이브코딩 실서버 배포와 DNS 연결 A to Z: 초보자가 겪는 7가지 함정과 해결법",
            "summary": (
                "Cursor, Claude로 만든 서비스를 도메인 구매부터 DNS A 레코드 연결, "
                "Nginx 리버스 프록시, HTTPS 자물쇠, Django WhiteNoise 정적 파일 설정까지 "
                "실서버 배포에 필요한 전 과정을 알기 쉽게 총정리합니다."
            ),
            "body_markdown": BODY_MARKDOWN,
            "category": "solo_dev",
            "tags": "바이브코딩,서버배포,도메인연결,DNS,Nginx,HTTPS,Django,WhiteNoise",
            "seo_title": "바이브코딩 실서버 배포 & 도메인 DNS 연결 완벽 가이드",
            "seo_description": (
                "도메인 구매 후 DNS A 레코드 설정, Nginx 리버스 프록시, Let's Encrypt HTTPS, "
                "Django WhiteNoise 정적 파일 서빙까지 초보자 눈높이 배포 절차입니다."
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
