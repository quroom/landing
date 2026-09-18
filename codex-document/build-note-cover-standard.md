# 빌드노트 대표 이미지 제작 표준

## 목적

목록 썸네일, 상세 본문, SNS 공유, `BlogPosting.image`에서 함께 사용할 대표 이미지를 일관되게 만든다. 검색 노출을 보장하는 장치가 아니라 글의 주제와 이미지를 명확하게 연결하는 보조 신호다.

## 고정 규격

- PNG 1200×630, 가급적 100KB 이하. 편집 원본은 같은 이름의 SVG로 보관한다.
- Noto Sans CJK KR 사용. 제목은 Bold, 보조 문구는 Regular 또는 Medium.
- 구성: 상단 `QUROOM`, 주제별 단순 아이콘, 짧은 kicker, 한 줄 핵심 제목, 키워드 3개, 하단 `BUILD NOTES`.
- 이미지 내부 제목은 작은 썸네일에서도 읽히도록 짧게 쓴다. 본문 제목 전체를 복사하지 않는다.
- 글마다 아이콘·배경색·강조색은 바꾸되 크기, 여백, 타이포그래피 체계는 유지한다.
- 사진, 생성형 이미지, 복잡한 설명 도표는 기본값으로 사용하지 않는다.
- `alt`는 글 주제와 핵심 키워드를 자연스럽게 설명한다.

## 파일과 재생성

- SVG 원본: `landing/static/landing/images/build-notes/sources/`
- 배포 PNG: `landing/static/landing/images/build-notes/`
- 렌더링: `python3 scripts/build-note-covers.py`
- 렌더링 후 `./scripts/verify.sh`와 모바일 화면 검증을 수행한다.

## 신규 글 체크리스트

1. `landing/build_note_images.py`에 slug, 이미지 키, alt, caption을 등록한다.
2. 기존 SVG 하나를 복사해 주제 아이콘, 배경색, kicker, 제목, 키워드를 바꾼다.
3. PNG를 생성하고 작은 크기로 축소해 제목 가독성을 확인한다.
4. 본문과 관계없는 키워드나 과장된 문구를 넣지 않는다.
5. 상세 페이지의 OG 이미지와 `BlogPosting.image`가 같은 절대 URL인지 확인한다.
