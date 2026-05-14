## Contributing

[fork]: https://github.com/github/REPO/fork
[pr]: https://github.com/github/REPO/compare

Hi there! We're thrilled that you'd like to contribute to this project. Your help is essential for keeping it great.

Contributions to this project are [released](https://help.github.com/articles/github-terms-of-service/#6-contributions-under-repository-license) to the public under the [project's open source license](LICENSE.txt).

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

---

## Walk Workflow (AI Engineering Track)

This repo uses a **plan-first, multi-file** contribution workflow at the Walk level. Follow these steps for every Walk exercise PR.

### Branch naming

```
walk/<your-github-id>/ex<N>-<short-name>
```

Each Walk branch chains off the previous exercise's branch. The PR base is always the prior exercise branch (not `main`).

### Workflow steps

1. **Write the plan first** — before touching any code, list every file you'll change and why. Include this plan in the PR description.
2. **Produce diffs file-by-file** — one file at a time, keeping scope to 2–4 files per PR.
3. **Run tests** — from `samples/book-app-project/`, run:
   ```
   pytest -v
   ```
   All tests must pass before committing.
4. **Capture evidence** — include test output (pass count, coverage %) in the PR description.
5. **Commit and push** — use descriptive commit messages that reference the exercise (e.g. `Walk Ex 4: add CONTRIBUTING + walk-onboarding`).
6. **Open PR** — use `gh pr create` with `--base` set to the prior exercise branch.

### PR structure (required sections)

```
## Plan
- Steps and files changed

## Evidence
- Test command + result summary

## Risk and Rollback
- Risk level
- Rollback: git revert <SHA>

## Track
- Level: Walk
- Exercise: Ex<N>
```

### Running tests locally

```powershell
cd samples/book-app-project
pytest -v
```

For coverage output:
```powershell
pytest -v --cov=. --cov-report=term-missing
```

See [ai-track-docs/walk-onboarding.md](ai-track-docs/walk-onboarding.md) for a full onboarding guide.
