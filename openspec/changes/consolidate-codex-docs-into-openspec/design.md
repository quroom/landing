## Context

- 현재 작업 문서(랜딩 명세, 바이브코딩 가이드/프롬프트 등)가 `codex-document/`에 흩어져 있어 OpenSpec 흐름과 분리됨.
- 이 변경(`consolidate-codex-docs-into-openspec`) 안으로 문서를 옮겨 단일 변경 히스토리와 아카이빙을 확보하려 함.
- 대상 문서: `codex-document/quroom-landing-spec.md`, `quroom-landing-openspec.md`, `general-vibe-coding-guide-for-beginners.md`, `vibe-coding-prompt-library.md`, `vibe-coding-step-by-step-guide.md`.

## Goals / Non-Goals

**Goals:**
- 문서들을 OpenSpec 변경 폴더로 이동/정리하여 단일 소스 확보.
- 기존 위치에는 포인터/README 안내를 남겨 경로 변경을 알림.
- 향후 아카이브/기본 명세와의 연계를 쉽게 만들 구조 제안.

**Non-Goals:**
- 문서 내용 대규모 개정이나 번역은 범위 밖.
- 코드/런타임 기능 추가 없음.

## Decisions

1) 새 위치  
   - 모든 문서를 `openspec/changes/consolidate-codex-docs-into-openspec/docs/` 하위로 이동. 파일명은 그대로 유지해 참조 용이성을 확보.

2) 원본 처리 방식  
   - `codex-document/`에는 동일 파일명을 가진 짧은 포인터 README(또는 단일 README 리스트)를 남겨 새 위치를 안내. 실 파일은 이동 후 제거.

3) 링크 관리  
   - 내부 상대 링크는 이동 후 깨질 수 있음: README(루트)와 포인터 README에서 새 절대/상대 경로를 명시. 문서 내부 링크는 이번 단계에선 영향 최소화를 위해 경로 안내만 제공(필요 시 후속 task로 수정).

4) 이미지/자산  
   - 현재 이미지는 `images/portfolio/...`에 있으므로 이동 불필요. 문서 이동 시 경로는 그대로 동작(리포 상대 경로).

5) 아카이브 전략  
   - 이 변경 완료 후 `openspec/changes/...`는 아카이브 대상이며, 메인 사양으로 승격 시 `openspec/specs/` 또는 별도 `docs/`로 동기화하는 추가 change에서 처리.

## Risks / Trade-offs

- [링크 단절] 문서 내부 상대 링크가 깨질 수 있음 → 포인터 README에 새 경로를 명시하고, 후속 작업으로 링크 일괄 수정.
- [외부 참조] 외부에서 `codex-document/` 경로를 북마크한 경우 혼란 → 포인터 README 유지로 완화.
- [중복 히스토리] 파일 이동으로 `git blame` 경로 변경 → `git mv`로 이동하여 히스토리 보존.

## Migration Plan

1. `openspec/changes/consolidate-codex-docs-into-openspec/docs/` 생성.
2. 대상 문서를 `git mv`로 이동.
3. `codex-document/`에 포인터 README 생성(새 경로 안내, 목록 제공).
4. 루트 `README.md`에 새 위치 안내 섹션 추가.
5. 상태 점검: 파일 존재/경로 확인.

## Open Questions

- 포인터 README를 각 파일별로 둘지, 단일 인덱스로 둘지? (현재는 단일 인덱스 방향 권장)
- 문서 내부 링크를 이번 변경에서 바로 수정할지, 후속 change로 분리할지? (작은 변경 유지 위해 후속으로 분리 제안)
