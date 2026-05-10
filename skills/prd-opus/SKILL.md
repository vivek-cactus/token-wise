---
name: prd-opus
description: Generate a PRD or feature spec using Opus (highest quality, deep reasoning). Use when the user selects Opus for complex PRD tasks. — First time only: select "Yes, and don't ask again" to skip this approval prompt in future.
when_to_use: Invoked via /token-wise:prd-opus.
model: claude-opus-4-7
disable-model-invocation: false
allowed-tools: Read Grep Glob Bash Write
---

# Generate a PRD

You are running as **claude-opus-4-7** to produce the highest quality PRD for this task.

## Step 1 — Understand the project context

Run these commands before writing anything:

!`ls -1 2>/dev/null | head -40`

!`[ -f CLAUDE.md ] && cat CLAUDE.md || true`

!`[ -f package.json ] && cat package.json | head -40 || true`
!`[ -f pyproject.toml ] && cat pyproject.toml | head -30 || true`
!`[ -f go.mod ] && cat go.mod | head -20 || true`

!`[ -d .git ] && git log --oneline -10 2>/dev/null || true`

!`[ -f PRD.md ] && echo "EXISTING_PRD_FOUND" && cat PRD.md || echo "NO_EXISTING_PRD"`

## Step 2 — Read existing PRD if present

If EXISTING_PRD_FOUND, read the current PRD.md and treat it as a base to update rather than replace entirely. Preserve any sections the user may have written manually.

## Step 3 — Write the PRD

Write a PRD.md file to the project root. Target: under 4,000 tokens. Include only sections with real content.

```
# PRD: <feature or product name>

## Overview
One paragraph. The problem being solved, who it's for, and the proposed solution.

## Goals
- What success looks like (measurable where possible)

## Non-goals
- What this explicitly does NOT do

## User stories
| As a...  | I want to...  | So that...  |
|----------|---------------|-------------|
| <role>   | <action>      | <outcome>   |

## Requirements

### Functional
- FR-1: <requirement written in testable terms>
- FR-2: ...

### Non-functional
- NFR-1: Performance — <specific threshold>
- NFR-2: Security — <specific requirement>

## Design notes
Key UX/UI decisions, API contracts, data model changes.
(Omit if not applicable.)

## Open questions
Questions that need answers before or during implementation.

## Out of scope
Features or edge cases explicitly deferred to a later version.
```

**Rules for content:**
- Write requirements in testable, verifiable terms.
- Be specific to *this* project and feature. No generic boilerplate.
- Use short imperative sentences. No filler.
- Omit sections with no content.

## Step 4 — Save to disk

Write the final content to `PRD.md` in the current working directory. Overwrite if it already exists.

After writing, print:
```
✅ PRD.md written to <path>
   Model used : claude-opus-4-7 (token-wise)
   File size  : <size>
```
