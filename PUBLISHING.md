# Publishing Guide

This directory lives inside a larger workspace repository, so publish it as its own standalone GitHub repository rather than pushing the parent workspace.

## Recommended Flow

1. Create a new empty GitHub repository, for example `one-person-company`
2. In this directory, initialize a nested repository
3. Commit the skill package
4. Add the GitHub remote
5. Push the first release

## Commands

Run these commands from this directory:

```bash
cd /home/living/.openclaw/workspace/one-person-company
git init
git checkout -b main
git add .
git commit -m "release: publish one-person-company v0.2.0"
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

If `main` already exists locally, skip the branch creation step.

## Suggested First Repository Settings

- repository name: `one-person-company`
- visibility: public
- description: `Set up and run a solo SaaS like a real company`
- homepage: optional, add the ClawHub listing later if desired
- topics: `ai-agents`, `solo-founder`, `saas`, `indie-hacker`, `workflow`, `openclaw`, `product-ops`

## Suggested First Release

- tag: `v0.2.0`
- title: `v0.2.0: first public release`
- notes source: `CHANGELOG.md` and `RELEASE-NOTES.md`

## ClawHub Submission Prep

Use the materials in `release/`:

- `clawhub-listing.md`
- `sample-outputs.md`
- `media-kit.md`
- `social-posts.md`
- the SVG assets under `release/assets/`

## Language Behavior To Mention Publicly

- Chinese prompt in, Chinese materials out by default
- English prompt in, English materials out by default
- bilingual output only when explicitly requested
