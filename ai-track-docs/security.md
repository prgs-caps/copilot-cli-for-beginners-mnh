# Security & Secrets Hygiene

## What was checked

- `.gitignore` reviewed for common secret file patterns
- Repo history scanned for `.env`, key, and credential files — none found
- `books.py` reviewed for hardcoded secrets — none found
- Runtime data file (`data.json`) checked for ignore coverage

## What was improved

| Item | Action |
|------|--------|
| Missing key/cert patterns (`*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.cer`, `*.crt`, `*.der`) | Added to `.gitignore` |
| Missing credential file patterns (`secrets.json`, `credentials.json`, `serviceaccount.json`) | Added to `.gitignore` |
| `samples/book-app-project/data.json` (runtime user data) | Added to `.gitignore` — prevents accidental commit |

## What was already in place

- `.env` and all `.env.*` variants already ignored
- No third-party secrets management needed (no network calls, no auth)

## Ongoing guidance

- Never commit credentials, tokens, or keys — use environment variables or a secrets manager.
- If `data.json` ever needs to be seeded for development, use a separate `data.example.json` that is committed without real data.
