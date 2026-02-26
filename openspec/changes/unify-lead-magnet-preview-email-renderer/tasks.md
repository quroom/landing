## 1. Shared Section Contract

- [x] 1.1 Extract a channel-neutral section AST builder for lead-magnet summary/weakest-category/2-week-action/CTA content.
- [x] 1.2 Route preview data construction through the shared section AST builder.
- [x] 1.3 Route email text/HTML rendering through the same section AST contract.

## 2. CTA Normalization and Rendering Consistency

- [x] 2.1 Consolidate `#contact` normalization into a single helper used by preview and email paths.
- [x] 2.2 Keep section order and headings synchronized across preview and email renderers.

## 3. Regression Safety

- [x] 3.1 Add section-level equivalence tests for shared preview/email output (titles/order/CTA target).
- [x] 3.2 Add text snapshot coverage for rendered copy to detect regression in wording/line breaks.
- [x] 3.3 Run `./scripts/verify.sh` and confirm the change is apply-ready and test-green.
