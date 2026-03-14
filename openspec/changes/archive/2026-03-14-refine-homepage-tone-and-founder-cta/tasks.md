## 1. Copy Audit And Founder-First Rewrite

- [x] 1.1 Audit homepage Hero, About, service summaries, and Contact copy for tool-first or internally phrased language.
- [x] 1.2 Rewrite founder-facing copy in `landing/content.py` so founder problems, execution outcomes, and accountable scope appear before internal tools or approaches.
- [x] 1.3 Keep foreign-developer references on `/` as secondary routing only, without detailed mixed messaging.

## 2. CTA Hierarchy Update

- [x] 2.1 Update homepage Hero in `landing/templates/landing/index.html` so `상담 문의하기` is the dominant CTA.
- [x] 2.2 Reduce the visual weight of `무료 자동화 실행 진단` and `서비스 보기` so they remain secondary actions.
- [x] 2.3 Simplify Contact-area CTA explanation to reduce choice overload and keep consultation as the default next step.

## 3. Verification

- [x] 3.1 Update tests affected by changed founder/foreign copy and CTA hierarchy.
- [x] 3.2 Run `./scripts/verify.sh`.
