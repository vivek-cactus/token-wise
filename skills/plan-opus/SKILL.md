---
name: plan-opus
description: Generate a project plan using Opus (highest quality, deep reasoning). Use when the user selects Opus for complex planning tasks. — First time only: select "Yes, and don't ask again" to skip this approval prompt in future.
when_to_use: Invoked via /token-wise:plan-opus.
model: claude-opus-4-7
disable-model-invocation: false
allowed-tools: Read Grep Glob Bash Write
---

# Generate a Plan

You are running as **claude-opus-4-7** to produce the highest quality plan for this task.

## Step 1 — Understand the project context

Run these commands before writing anything:

!`ls -1 2>/dev/null | head -40`

!`[ -f CLAUDE.md ] && cat CLAUDE.md || true`

!`[ -f package.json ] && cat package.json | head -40 || true`
!`[ -f pyproject.toml ] && cat pyproject.toml | head -30 || true`
!`[ -f go.mod ] && cat go.mod | head -20 || true`
!`[ -f Cargo.toml ] && cat Cargo.toml | head -30 || true`

!`[ -d .git ] && git log --oneline -10 2>/dev/null || true`

!`[ -f PLAN.md ] && echo "EXISTING_PLAN_FOUND" && cat PLAN.md || echo "NO_EXISTING_PLAN"`

## Step 2 — Identify the plan type

Based on the user's prompt, determine which kind of plan to write:

- **Architecture plan**: System design, components, data flow, tech decisions
- **Sprint plan**: Concrete tasks, estimates, priorities, acceptance criteria
- **Feature plan**: Step-by-step breakdown of a single feature
- **Roadmap**: Phased delivery milestones across time

If EXISTING_PLAN_FOUND, treat the existing PLAN.md as a base to update rather than replace entirely.

## Step 3 — Write the plan

Write a PLAN.md file to the project root. Include only sections with real content.

```
# Plan: <goal or feature name>

## Objective
One paragraph. What this plan achieves and why.

## Scope
What is in scope. What is explicitly out of scope.

## Architecture / Design
Key components, interactions, data flow. ASCII diagrams if helpful.
(Omit if this is a sprint or task plan.)

## Phases / Milestones
### Phase 1: <name>
- Task 1
- Task 2

### Phase 2: <name>
- Task 1

## Task breakdown (for sprint plans)
| # | Task | Effort | Priority | Depends on |
|---|------|--------|----------|------------|
| 1 | ...  | S/M/L  | P0–P3    | —          |

## Risks & Assumptions
- Risk: ...
- Assumption: ...

## Success criteria
How we know this plan is complete.
```

**Rules for content:**
- Be specific to *this* project. No generic advice.
- Use short imperative sentences.
- Prefer tables and lists over prose.
- Every task must be something a developer can pick up and act on.
- If a section would be empty, omit it.

## Step 4 — Save to disk

Write the final content to `PLAN.md` in the current working directory. Overwrite if it already exists.

After writing, print:
```
✅ PLAN.md written to <path>
   Model used : claude-opus-4-7 (token-wise)
   File size  : <size>
```
