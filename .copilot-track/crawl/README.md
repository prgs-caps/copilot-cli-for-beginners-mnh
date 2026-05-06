# Crawl Track — README

This folder tracks state for the **Crawl** level of the AI Engineering track.

## What is the Crawl level?

You use GitHub Copilot as an **assistant** — inline suggestions, `/explain`, `/tests` — on a single file or module at a time.

---

## Key Concepts

### Chain-PRs

Each exercise builds on the previous one. Branches are chained:

```
main
 └── crawl/prgs-caps/ex0-bootstrap
      └── crawl/prgs-caps/ex1-orientation
           └── crawl/prgs-caps/ex2-baseline
                └── ...
```

Always branch off the **previous exercise's branch**, not `main`.

### Evidence in PRs

Every PR must include evidence that the change works. Evidence means:
- Test output (copy/paste the passing run)
- Logs or metrics where tests don't apply
- A rollback plan (e.g. "revert commit SHA" or "toggle flag X")

No evidence = incomplete PR.

### Prompt Usage

Each exercise provides a **prompt block** — copy it in full and send it to Copilot Chat. The prompt tells Copilot:
1. What to build
2. To propose the smallest safe plan first
3. To list files, generate diffs, adjust tests, and draft the PR description

Do not paraphrase the prompt. Copy it exactly.
