# AI Review Checklist — Run Ex 11

**Date:** 2026-05-14  
**PR reviewed:** Run Ex 10 — CI Reliability Improvements (PR #41)  
**Reviewer:** GitHub Copilot (simulated AI review)  
**Files in scope:** `.github/workflows/book-app-ci.yml`, `ai-track-docs/ci-reliability.md`

---

## Review Focus

The three changes introduced in Ex 10 are each independently safe and additive. The review focuses on:

1. **Correctness of pip cache path** — does `cache-dependency-path` resolve correctly relative to the repo root?
2. **Timeout adequacy** — is 10 minutes appropriate given the suite's runtime?
3. **Impact of removing `continue-on-error`** — could this silently break anything downstream?
4. **Trigger scope** — `on: push` with no branch filter; is this intentional?
5. **Action version pinning** — major-version tags vs. SHA pins.

---

## Findings

### Finding 1 — PASS: `cache-dependency-path` resolves correctly ✅

```yaml
cache-dependency-path: samples/book-app-project/pyproject.toml
```

`cache-dependency-path` is evaluated from the **repository root**, not from `defaults.run.working-directory`. The path `samples/book-app-project/pyproject.toml` correctly points to the only `pyproject.toml` in scope. The cache key will change whenever `pyproject.toml` is modified, which is the desired behavior.

**No action required.**

---

### Finding 2 — PASS: 10-minute timeout is appropriate ✅

The test suite completes in < 1 second locally and < 60 seconds in CI (including setup). A 10-minute cap provides a 10× safety margin against transient slowness while still preventing indefinite hangs.

If a future test introduces network calls or large fixtures, raise `timeout-minutes` in the same PR that adds that test.

**No action required.**

---

### Finding 3 — PASS: Removing `continue-on-error` is the correct hardening ✅

Before Ex 10, a failing test run would not fail the CI job — reviewers had no automatic red signal. The `Post coverage summary` step already has `if: always()`, so coverage output is still posted even when the test step fails. No downstream consumer depended on the always-green behavior.

**Response:** Change is correct. The PR description notes this explicitly.

---

### Finding 4 — NOTE: `on: push` has no branch filter ⚠️

```yaml
on:
  push:
  pull_request:
```

This configuration was present **before** Ex 10 and was not changed in this PR. It causes the CI job to run on every push to every branch, including draft branches and bot-created branches. This is not a defect introduced here, but it is worth noting for a future cleanup.

**Suggested future action:** Scope `push` to protected branches:
```yaml
on:
  push:
    branches: [main]
  pull_request:
```

Tracked as a future backlog item — out of scope for Ex 10.

---

### Finding 5 — NOTE: Actions pinned to major-version tags, not SHAs ⚠️

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
```

Major-version tags (`@v4`, `@v5`) can be silently updated by the action author. For stronger supply-chain integrity, pin to a specific commit SHA:

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
- uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b  # v5.3.0
```

This was pre-existing behavior and is out of scope for Ex 10. Tracked for a future security sweep.

**No action required in this PR.**

---

## Verification Steps

To verify Ex 10 changes are working correctly after merge:

1. **Confirm cache is active:**  
   In the GitHub Actions run log, look for:  
   `Cache restored successfully` under the `Set up Python` step.  
   On the first run after the PR merges you will see `Cache not found` (cache miss) followed by `Cache saved` — subsequent runs will show a hit.

2. **Confirm timeout is enforced:**  
   The job detail page shows `timeout-minutes: 10` in the job header. A hung run will show `Job cancelled (exceeded timeout)`.

3. **Confirm test gate is hard:**  
   Introduce a deliberate test failure on a branch, push it, and confirm the CI job shows ✗ (not ✓ with a warning). Revert before merging.

4. **Confirm coverage summary still posts on failure:**  
   The `Post coverage summary` step uses `if: always()` — it should appear in the job summary even when the test step fails.

---

## Risk Assessment

| Area | Risk | Notes |
|------|------|-------|
| Pip caching | Low | Cache misses fall back to full install; no correctness risk |
| Job timeout | Low | 10 min >> expected runtime; raise if needed |
| Remove continue-on-error | Low-Medium | Breaks "always green" assumption — intentional and documented |
| Action version pinning | Low | Pre-existing; not introduced in this PR |

**Overall: Low risk. Changes are correct, additive, and well-documented.**

---

## Reviewer Response to Findings

| Finding | Status | Action |
|---------|--------|--------|
| Cache path resolves correctly | ✅ Confirmed | None |
| Timeout adequate | ✅ Confirmed | None |
| continue-on-error removal correct | ✅ Confirmed | None |
| Branch filter missing on `push` | ⚠️ Pre-existing | Backlog item for future security/CI sweep |
| Action SHA pinning absent | ⚠️ Pre-existing | Backlog item for future security sweep |

---

## How to Reuse This Checklist

Apply this pattern to any PR touching `.github/workflows/`:

1. **Correctness** — do paths and environment assumptions hold?
2. **Timeout** — is the cap appropriate for the job's expected runtime?
3. **Gate hardness** — are failures actually failing the job?
4. **Trigger scope** — is the workflow running on the right branches/events?
5. **Supply chain** — are actions pinned appropriately?

Template location: `ai-track-docs/ai-review-checklist.md`
