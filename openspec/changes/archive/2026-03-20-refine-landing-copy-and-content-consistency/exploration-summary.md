# Exploration Summary

Date: 2026-03-20

## Current Code State

- Latest homepage micro-copy work was pushed to `main` in commit `6403643` (`Polish homepage copy phrasing`).
- The actual implementation scope is small:
  - remove `Official` labeling from the homepage shell
  - soften a few homepage founder phrases in `landing/content.py`
  - update homepage assertions in `landing/tests/test_landing_pages.py`
- No broader homepage rewrite was implemented.

## Current OpenSpec State

- Active change: `refine-landing-copy-and-content-consistency`
- Status in OpenSpec: `in-progress`
- Tasks remain `0/8`

## Mismatch We Observed

The current code and the current change artifacts are not at the same level.

```text
implemented reality
  └─ micro-copy polish only

current change artifacts
  └─ broader founder homepage rewrite
     - Hero/About/Services/Contact tone realignment
     - trust-policy absorption
     - service summary reframing
     - founder-route language alignment
```

This means the open change is now larger than the user's current preference.

## Options Discussed

### Option A: Shrink the existing change to match reality

Interpret the active change as a narrow homepage micro-copy polish effort.

Pros:
- keeps a single change history for the same homepage area
- aligns docs with what the user actually wanted
- avoids leaving a misleading broad rewrite change open

Cons:
- the current proposal/design ambition has to be reduced

### Option B: Treat the homepage as done and close or pause the change

Accept the current pushed copy as sufficient and stop homepage work for now.

Pros:
- minimal additional process work
- avoids overworking copy the user already found too strong

Cons:
- the active change still needs cleanup, pause, or redefinition

### Option C: Continue the broad rewrite as originally proposed

Pros:
- preserves the original idea behind the change

Cons:
- conflicts with recent user feedback favoring only small copy adjustments
- likely to reintroduce tone problems

## Recommendation

Recommended path: **Option A**

```text
keep the active change
        ↓
reduce its scope
        ↓
document it as micro-copy polish
        ↓
only then decide whether more homepage copy work is needed
```

If the user feels the homepage is already good enough, Option B is the clean fallback.

## Suggested Next Conversation

1. Decide whether the homepage needs any more copy changes at all.
2. If yes, constrain it to `3-5` sentences maximum.
3. Update the active change artifacts to match that narrow scope.
4. If no, redefine or close the active change rather than leaving it broad and pending.
