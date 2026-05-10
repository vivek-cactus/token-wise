---
name: readme-opus
description: Generate or update a README using Opus (highest quality). Use when the user selects Opus for README tasks. — First time only: select "Yes, and don't ask again" to skip this approval prompt in future.
when_to_use: Invoked via /token-wise:readme-opus.
model: claude-opus-4-7
disable-model-invocation: false
allowed-tools: Read Grep Glob Bash Write
---

# Generate README

You are running as **claude-opus-4-7** to produce the highest quality README for this project.

## Step 1 — Discover the project

!`[ -f README.md ] && echo "EXISTING_README_FOUND" || echo "NO_EXISTING_FILE"`

!`ls -1 2>/dev/null | head -40`

!`[ -f package.json ] && cat package.json | head -60 || true`
!`[ -f composer.json ] && cat composer.json | head -40 || true`
!`[ -f Cargo.toml ] && cat Cargo.toml | head -30 || true`
!`[ -f pyproject.toml ] && cat pyproject.toml | head -30 || true`
!`[ -f go.mod ] && cat go.mod | head -20 || true`

!`[ -f CLAUDE.md ] && cat CLAUDE.md || true`

!`[ -d .git ] && git log --oneline -5 2>/dev/null || true`
!`[ -d .git ] && git remote -v 2>/dev/null | head -4 || true`

## Step 2 — Read existing README if present

If EXISTING_README_FOUND, read the current README.md and treat it as a base to update rather than replace. Preserve any sections the user may have written manually.

## Step 3 — Write the README

Write a README.md file to the project root. Keep it concise and developer-focused.

```
# <Project Name>

> One-sentence tagline — what it does and who it's for.

## Overview
2–3 sentences. The problem it solves and the approach.

## Features
- Feature 1
- Feature 2

## Quick start

\`\`\`bash
# Install
npm install   # or: pip install, cargo build, go install, etc.

# Configure
cp .env.example .env

# Run
npm start
\`\`\`

## Usage

Brief example showing the most common use case. Code block preferred.

## Configuration

| Variable   | Description          | Default  |
|------------|----------------------|----------|
| `VAR_NAME` | What it controls     | `value`  |

## Contributing

Short contribution guide. Link to CONTRIBUTING.md if it exists.

## License

<license name> — see [LICENSE](./LICENSE)
```

**Rules for content:**
- Write what is true about *this* project specifically. No boilerplate filler.
- Prefer code blocks over prose for setup steps.
- Keep the Quick start section runnable with copy-paste.
- If a section would be empty, omit it.

## Step 4 — Save to disk

Write the final content to `README.md` in the current working directory. Overwrite if it already exists.

After writing, print:
```
✅ README.md written to <path>
   Model used : claude-opus-4-7 (token-wise)
   File size  : <size>
```
