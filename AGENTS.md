## Project Instructions

- After completing any code changes, run `./scripts/verify.sh` before sending the final response.
- Use `.venv` Python for Django commands via scripts in `scripts/`.
- If verification cannot run, report the exact blocker in the final response.
- For Naver Powerlink dynamic landing and attribution work, read `openspec/changes/align-naver-powerlink-landing-attribution/` first. Treat `/home/quroom/workspace/ad-for-everthing/naver/inputs/ad_creatives.csv` as the source of truth for ad creative URL intent, and keep UTM analytics parameters separate from `src/campaign/group/intent/creative/kw` landing-control parameters.
