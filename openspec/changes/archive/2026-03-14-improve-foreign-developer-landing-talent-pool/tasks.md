## 1. Content and CTA restructuring

- [ ] 1.1 Update foreign-developer hero copy to stage-based messaging (remove fixed-duration promise)
- [ ] 1.2 Replace single primary CTA with first-stage quick-intake CTA copy and helper text
- [ ] 1.3 Add second-stage matching-profile CTA entry point and explanatory copy
- [ ] 1.4 Update FAQ and boundary copy to include non-guaranteed placement and profile-fit introduction policy
- [ ] 1.4a Add regional support copy for Gwangju/Jeonnam in-person priority and online-first support for other regions
- [ ] 1.5 Add community-sharing section copy and waitlist CTA with scope boundary note
- [ ] 1.6 Add waitlist policy copy that explains channel launch threshold criteria
- [ ] 1.7 Align foreign-developer nav and service-card copy with strategy-first positioning
- [ ] 1.8 Reduce founder homepage hero CTA competition so consultation remains the primary action

## 2. Form and submission flow

- [ ] 2.1 Define first-stage quick-intake field set: required (`nickname`, `email`, `target_role`) + optional (`notes`)
- [ ] 2.2 Define second-stage matching-profile required fields: `cv_or_linkedin`, `github_or_portfolio`, `tech_stack`, `experience_level`, `visa_status`, `work_preference`, `location_preference`, `available_from`
- [ ] 2.3 Implement separated submission handling for stage one and stage two flows
- [ ] 2.4 Ensure stage-two submission is linked to existing candidate/inquiry lifecycle
- [ ] 2.5 Keep existing founder flow unaffected and regression-check persona branching

## 3. Data persistence and lifecycle tracking

- [ ] 3.1 Extend inquiry persistence to store funnel stage and lifecycle state for foreign-developer leads
- [ ] 3.2 Add lifecycle transitions (new, strategy_in_progress, matching_pending, intro_in_progress, closed)
- [ ] 3.3 Surface lifecycle state in admin/operational query paths used by dashboard reports
- [ ] 3.4 Create migration and fallback handling for pre-existing foreign-developer inquiries

## 4. Analytics and measurement

- [ ] 4.1 Add stage-specific funnel events for quick intake, profile completion, and introduction start
- [ ] 4.2 Update funnel reporting logic to compute stage conversion rates for foreign-developer journey
- [ ] 4.3 Validate event payload includes page key, lead source, and stage context consistently
- [ ] 4.4 Add community waitlist submit event and report waitlist growth trend

## 5. QA and rollout readiness

- [ ] 5.1 Add/adjust tests for staged CTA rendering and localization behavior on `/for-foreign-developers/`
- [ ] 5.2 Add/adjust tests for stage-one and stage-two submission persistence and lifecycle transitions
- [ ] 5.3 Perform manual copy review for expectation boundary placement near CTA/FAQ/form
- [ ] 5.4 Run full verification script and document rollout/rollback checklist
