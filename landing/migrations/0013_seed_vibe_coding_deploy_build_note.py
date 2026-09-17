from django.db import migrations
from django.utils import timezone

BODY_MARKDOWN = """## 로컬에서는 잘 돌았는데, 서버에 올리니 먹통이 됩니다

최근 Cursor, Claude Code 등 AI 도구로 웹 서비스나 MVP를 3~5일 만에 완성하는 사례가 많아졌습니다. 화면과 로컬 로직은 빠르게 나오지만, 많은 분들이 **실서버(리눅스 VPS, Dokku, Cloudtype, AWS) 배포 단계**에서 며칠 동안 멈춰 서게 됩니다.

로컬 환경(`127.0.0.1:8000`)과 상용 리눅스 프로덕션 환경 사이에는 **보안 검증, 네트워크 소켓 바인딩, 정적 파일 서빙, RDBMS 마이그레이션 트랜잭션**이라는 엄격한 간극이 존재하기 때문입니다.

8년 차 풀스택 개발사로서 지난 수년간 Django 기반 상용 서비스를 운영·배포하며, AI로 생성한 코드에서 가장 빈번하게 터지는 4가지 실전 장애와 해결 방법을 명확한 설정 코드와 함께 정리합니다.

---

### 1. `DEBUG = False` 전환 시 스타일(CSS/JS) 증발

가장 흔하게 겪는 첫 번째 멘붕입니다. 로컬에서는 멀쩡하던 사이트가 실서버에 올리고 보안을 위해 `DEBUG = False`로 바꾸는 순간 90년대 텍스트 문서처럼 깨져버립니다.

#### 원인
Django의 내장 개발서버(`runserver`)는 `DEBUG = True`일 때 정적 파일(CSS, JS, 이미지)을 자동으로 서빙해 줍니다. 하지만 보안과 성능을 위해 실서버에서 `DEBUG = False`로 바꾸는 순간, Django는 정적 파일 서빙을 완전히 중단합니다.

#### 해결 절차
리눅스 서버 환경에서는 `whitenoise` 라이브러리를 사용해 정적 파일을 직접 고속 서빙하도록 구성하고, 배포 파이프라인에서 정적 파일 모으기(`collectstatic`)를 실행해야 합니다.

1. **WhiteNoise 미들웨어 등록 (`settings.py`)**:
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # SecurityMiddleware 바로 아래 배치
    # ... 기존 미들웨어들
]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

2. **배포 명령 실행**:
```bash
python manage.py collectstatic --noinput
```

---

### 2. 도메인 연결 직후 `400 Bad Request` & `403 Forbidden`

도메인을 구매해서 연결했더니 하얀 화면에 `Bad Request (400)`만 뜨거나, 문의 폼을 전송하면 `CSRF verification failed (403)`가 발생합니다.

#### 원인
Django는 호스트 헤더 위조 공격(Host Header Attack)과 크로스 사이트 요청 위조(CSRF)를 원천 차단하기 위해 엄격한 도메인 화이트리스트를 요구합니다.
- `ALLOWED_HOSTS`에 내 실제 도메인이 없으면 모든 요청을 `400`으로 튕겨냅니다.
- Django 4.0 이상부터는 HTTPS 환경에서 `CSRF_TRUSTED_ORIGINS`에 도메인을 등록하지 않으면 POST 요청을 `403`으로 차단합니다.

#### 해결 절차 (`settings.py`)
```python
# 구매한 도메인과 서브도메인을 명시
ALLOWED_HOSTS = ["quroom.kr", "www.quroom.kr", "localhost", "127.0.0.1"]

# HTTPS 프로토콜을 포함하여 등록 필수
CSRF_TRUSTED_ORIGINS = [
    "https://quroom.kr",
    "https://www.quroom.kr",
]
```

---

### 3. Nginx 502 Bad Gateway (Gunicorn 바인딩 오류)

Nginx 웹서버는 정상 동작하는데 브라우저에 접속하면 `502 Bad Gateway`가 떨어집니다.

#### 원인
Gunicorn(WSGI 서버)을 실행할 때 `127.0.0.1:8000`으로 바인딩한 경우, Docker 컨테이너나 격리된 네트워크 환경에서는 `127.0.0.1`이 컨테이너 내부 루프백 인터페이스만 가리킵니다. 따라서 컨테이너 바깥의 Nginx 리버스 프록시가 전달하는 요청을 전혀 수신하지 못합니다.

#### 해결 절차
Gunicorn 실행 명령에서 호스트 바인딩을 반드시 모든 네트워크 인터페이스를 뜻하는 `0.0.0.0`으로 열어주어야 합니다.

```bash
# Procfile 또는 Docker 실행 명령
gunicorn --workers=2 --threads=2 --bind 0.0.0.0:8000 landing.project.wsgi:application
```

Nginx 설정(`nginx.conf`)에서는 클라이언트의 실제 IP와 HTTPS 프로토콜 정보를 Django로 안전하게 전달하도록 프록시 헤더를 전달합니다:
```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

### 4. 로컬 SQLite ➡️ 실서버 PostgreSQL 전환 시 마이그레이션 충돌

로컬에서는 `db.sqlite3` 파일 하나로 아무 문제 없이 동작했는데, 실서버에서 PostgreSQL이나 MySQL을 붙이고 `python manage.py migrate`를 실행하면 `InconsistentMigrationHistory`나 컬럼 타입 불일치 에러로 서버 실행이 멈춥니다.

#### 원인
- SQLite는 데이터 타입 검사가 느슨하여 AI가 모델 필드를 뒤죽박죽 바꿔도 로컬에서는 그냥 돌아갑니다.
- 하지만 PostgreSQL은 외래키 제약조건(Foreign Key)과 타입 검사가 엄격합니다. AI에게 프롬프트로 필드 수정을 반복 요청하면서 마이그레이션 파일 간의 의존성(`dependencies = [...]`) 트리가 꼬이면 깨끗한 상용 DB에 적용할 때 충돌이 터집니다.

#### 해결 절차
배포 전 로컬에서 마이그레이션 상태를 전수 검증하고 정리해야 합니다:

```bash
# 마이그레이션 의존성 트리 전수 확인
python manage.py showmigrations

# 꼬인 마이그레이션 파일이 많다면 스쿼시(Squash)하여 단일 체인으로 압축
python manage.py squashmigrations landing 0010

# 실서버 배포 시 릴리즈 단계에서 자동 실행
python manage.py migrate --noinput
```

---

### 배포 전 1분 체크리스트

1. **정적 파일**: `WhiteNoise` 미들웨어 확인 + `collectstatic` 실행
2. **도메인 보안**: `ALLOWED_HOSTS`와 `CSRF_TRUSTED_ORIGINS`에 도메인 등록
3. **WSGI 바인딩**: Gunicorn을 `0.0.0.0:8000`으로 바인딩
4. **데이터베이스**: 배포 전 `showmigrations`로 마이그레이션 트리 무결성 검증

---

### 바이브코딩 배포 및 Django 아키텍처 점검이 필요하신가요?

화면은 만들었으나 실서버 배포, WhiteNoise 정적 파일 서빙, Nginx 502 오류, PostgreSQL 마이그레이션 충돌에서 막히셨다면 큐룸(QUROOM)의 **[15분 무료 코드·배포 진단](/free-diagnosis/)**을 신청해 주세요. 8년 차 풀스택 엔지니어가 직접 코드를 검토하고 실서버 배포 경로를 안내해 드립니다.
"""


def seed_vibe_coding_deploy_note(apps, schema_editor):
    BuildNote = apps.get_model("landing", "BuildNote")
    BuildNote.objects.update_or_create(
        slug="vibe-coding-deploy-troubleshooting",
        defaults={
            "title": "Django·AI 코드를 실서버에 배포할 때 발생하는 기술적 장애 4가지와 해결 절차",
            "summary": (
                "로컬 환경(127.0.0.1:8000)에서는 잘 돌던 Django 코드가 "
                "실서버 배포 시 CSS 깨짐, 400 에러, Nginx 502, PostgreSQL 충돌로 멈추는 "
                "4대 원인과 실전 해결 코드 스니펫을 정리합니다."
            ),
            "body_markdown": BODY_MARKDOWN,
            "category": "solo_dev",
            "tags": "Django,배포에러,WhiteNoise,Gunicorn,ALLOWED_HOSTS,PostgreSQL",
            "seo_title": "Django 실서버 배포 에러 4가지와 해결법 (WhiteNoise, Nginx, 마이그레이션)",
            "seo_description": (
                "Django 코드를 실서버에 배포할 때 발생하는 CSS 깨짐, 400 Bad Request, "
                "Gunicorn 502 Bad Gateway, PostgreSQL 마이그레이션 충돌 해결 절차입니다."
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
