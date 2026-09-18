"""Editorial diagrams shared by the offline renderer and article metadata."""

COVERS = {
    "vibe-coding-deploy-troubleshooting": (
        "deploy",
        "바이브코딩 실서버 배포 오류: DNS, Nginx, 정적 파일",
        "DNS · Nginx · 정적 파일",
    ),
    "self-hosted-dokku-vps-guide": (
        "dokku",
        "셀프 호스팅 Dokku VPS 배포: Git push, 컨테이너, SSL",
        "Git push · 컨테이너 · SSL",
    ),
    "portone-v2-webhook-idempotency-guide": (
        "webhook",
        "결제 웹훅 중복 결제 방지: 서명 검증, 멱등성, 금액 확인",
        "서명 검증 · 멱등성 · 금액 확인",
    ),
    "ai-prototype-refactoring-guide": (
        "refactoring",
        "AI 프로토타입 상용화 리팩터링: 코드 진단, 경계 분리, 테스트",
        "코드 진단 · 경계 분리 · 테스트",
    ),
    "outsourcing-contract-wbs-out-of-scope-guide": (
        "scope",
        "외주 계약 과업 범위와 검수 기준: 포함 범위, 제외 범위, 인수 조건",
        "포함 범위 · 제외 범위 · 인수 조건",
    ),
    "mvp-development-cost-breakdown": (
        "mvp-cost",
        "린 MVP 개발 견적 구성: 기능 분해, 공수 산정, 검증 비용",
        "기능 분해 · 공수 산정 · 검증 비용",
    ),
    "building-from-features-fails": (
        "discovery",
        "제품 기획에서 기능보다 문제 정의: 사용자 문제, 가설, 최소 실험",
        "사용자 문제 · 가설 · 최소 실험",
    ),
}
COVERS["기능부터-시작하면-망합니다"] = COVERS["building-from-features-fails"]


def cover_for_slug(slug):
    cover = COVERS.get(slug)
    if cover is None:
        return None
    key, alt, caption = cover
    return {
        "path": f"landing/images/build-notes/{key}.png",
        "alt": alt,
        "caption": caption,
    }
