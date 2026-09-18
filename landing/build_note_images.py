"""Editorial diagrams shared by the offline renderer and article metadata."""

COVERS = {
    "vibe-coding-deploy-troubleshooting": (
        "deploy",
        "웹서비스 배포 경로",
        "브라우저 → DNS → 프록시 → 앱 서버",
        ("브라우저", "DNS", "프록시", "앱 서버"),
    ),
    "self-hosted-dokku-vps-guide": (
        "dokku",
        "Dokku 배포 흐름",
        "코드 변경에서 서비스 운영까지",
        ("Git push", "빌드", "컨테이너", "라우팅"),
    ),
    "portone-v2-webhook-idempotency-guide": (
        "webhook",
        "결제 웹훅 처리 흐름",
        "검증과 중복 확인 후 상태 반영",
        ("웹훅 수신", "서명 검증", "중복 확인", "상태 반영"),
    ),
    "ai-prototype-refactoring-guide": (
        "refactoring",
        "프로토타입 상용화 점검",
        "기존 코드에서 운영 가능한 구조로",
        ("코드 진단", "경계 분리", "테스트", "운영 점검"),
    ),
    "outsourcing-contract-wbs-out-of-scope-guide": (
        "scope",
        "외주 개발 범위 합의",
        "구현 범위와 인수 기준을 함께 정리",
        ("요구사항", "제외 범위", "작업 명세", "인수 검수"),
    ),
    "mvp-development-cost-breakdown": (
        "mvp-cost",
        "MVP 개발 견적 구성",
        "기능별 작업과 검증 비용 산정",
        ("핵심 기능", "작업 분해", "공수 산정", "검증·배포"),
    ),
    "building-from-features-fails": (
        "discovery",
        "제품 개발의 출발점",
        "문제 확인에서 작은 실험까지",
        ("사용자 문제", "가설", "최소 실험", "피드백"),
    ),
}
COVERS["기능부터-시작하면-망합니다"] = COVERS["building-from-features-fails"]


def cover_for_slug(slug):
    cover = COVERS.get(slug)
    if cover is None:
        return None
    key, title, subtitle, steps = cover
    return {
        "path": f"landing/images/build-notes/{key}.png",
        "alt": f"{title}: {' → '.join(steps)}",
        "caption": subtitle,
    }
