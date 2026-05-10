---
name: claude-md-opus
description: Generate or update CLAUDE.md using Opus (highest quality). Use when the user selects Opus for CLAUDE.md tasks. — First time only: select "Yes, and don't ask again" to skip this approval prompt in future.
when_to_use: Invoked via /token-wise:claude-md-opus.
model: claude-opus-4-7
disable-model-invocation: false
allowed-tools: Read Grep Glob Bash Write
---

# Generate CLAUDE.md

You are running as **claude-opus-4-7** to produce the highest quality CLAUDE.md for this project.

## Step 1 — Discover the project

Run these commands to understand the project before writing anything:

!`[ -f CLAUDE.md ] && echo "EXISTING_CLAUDE_MD_FOUND" || echo "NO_EXISTING_FILE"`

!`ls -1 2>/dev/null | head -40`

!`[ -f package.json ] && cat package.json | head -40 || true`
!`[ -f composer.json ] && cat composer.json | head -40 || true`
!`[ -f Cargo.toml ] && cat Cargo.toml | head -30 || true`
!`[ -f pyproject.toml ] && cat pyproject.toml | head -30 || true`
!`[ -f go.mod ] && cat go.mod | head -20 || true`

!`[ -f .env.example ] && cat .env.example | head -30 || true`
!`[ -f .env.local.example ] && cat .env.local.example 2>/dev/null | head -30 || true`

!`[ -d .git ] && git log --oneline -5 2>/dev/null || true`
!`[ -d .git ] && git remote -v 2>/dev/null | head -4 || true`

!`find . -name "*.info.yml" -path "*/modules/custom/*" 2>/dev/null | head -5 | xargs grep -l "type: module" 2>/dev/null || true`
!`find . -name "*.info.yml" -path "*/themes/custom/*" 2>/dev/null | head -3 || true`

## Step 2 — Read existing CLAUDE.md if present

If EXISTING_CLAUDE_MD_FOUND was printed above, read the current CLAUDE.md and treat it as a base to update rather than replace entirely. Preserve any manual sections the user may have written.

## Step 3 — Write CLAUDE.md

Write a CLAUDE.md file to the project root. Follow these rules strictly:

**Target: under 6,000 tokens total.** Every section must earn its place.

Use this structure — include a section only if there is real content to put in it:

```
# Project: <name>

## Overview
One paragraph. What the project does, who it is for, tech stack summary.

## Architecture
Key directories and what lives in them. Only non-obvious structure needs explanation.

## Development setup
Commands to install, configure, and run. Prerequisites if non-standard.

## Common tasks
The most frequent dev tasks as short numbered steps or commands. No fluff.

## Code conventions
Language/framework-specific rules that apply here. Naming, patterns to follow or avoid.

## Testing
How to run tests. Where tests live. Any known gotchas.

## Environment variables
List required env vars with a one-line description each. No values.

## Important constraints
Things Claude must never do in this project (e.g. never edit generated files, never commit secrets, always run linter before proposing a PR).
```

**Rules for content:**
- Write what is true about *this* project specifically. No generic advice.
- Use short imperative sentences. Omit "you should", "please", "make sure to".
- Prefer commands over prose wherever possible.
- If a section would be empty or identical to any standard framework default, omit it.
- Keep the Important constraints section to the most critical rules only (3–5 max).

## Step 4 — Save to disk

Write the final content to `CLAUDE.md` in the current working directory. Overwrite if it already exists.

After writing, print:
```
✅ CLAUDE.md written to <path>
   Model used : claude-opus-4-7 (token-wise)
   File size  : <size>
```
