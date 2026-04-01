# Contributing

## What Good Contributions Look Like

- improve the quality of reusable operating artifacts
- tighten role ownership and workflow clarity
- improve first-run usefulness for solo SaaS founders
- keep the trust boundary explicit for risky actions
- preserve the language behavior: Chinese in -> Chinese out, English in -> English out by default

## Before Opening A PR

- keep changes focused
- update `README.md` or `SAMPLE-OUTPUTS.md` when public behavior changes
- update `CHANGELOG.md` when the release surface changes
- run the helper scripts if you changed templates or script behavior

## Basic Validation

From the repository root:

```bash
python3 scripts/init_company.py "Acme Solo" --path /tmp/opc-check --mode saas
python3 scripts/weekly_review.py /tmp/opc-check/acme-solo --week-of 2026-03-30
```
