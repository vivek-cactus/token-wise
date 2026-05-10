# token-wise

A Claude Code plugin that routes text-heavy tasks to the right Claude model — saving tokens without sacrificing quality.

## Why

Planning, CLAUDE.md generation, README writing, and PRDs don't need Opus when you're just structuring content. token-wise intercepts these tasks and runs them on Sonnet or Haiku instead, switching back to your session model automatically when done.

## Quick start

```bash
# 1. Install
claude --plugin-dir /path/to/token-wise

# 2. Use model-specific commands
/token-wise:plan-haiku      # Plan on Haiku (fastest)
/token-wise:plan-sonnet     # Plan on Sonnet (balanced)
/token-wise:plan-opus       # Plan on Opus (highest quality)

/token-wise:readme-haiku    # README on Haiku
/token-wise:prd-sonnet      # PRD on Sonnet
/token-wise:claude-md-opus  # CLAUDE.md on Opus
```

## Choosing a model tier

| Model | Best for | Tradeoff |
|-------|----------|----------|
| **Haiku** | Simple, well-defined tasks (READMEs, straightforward plans) | Fastest & cheapest; less creative |
| **Sonnet** | Most tasks (balanced speed, quality, cost) | Good all-rounder; not specialized |
| **Opus** | Complex specs, architectural plans, high-stakes documentation | Highest quality; slower & costlier |

## Available skills

| Task | Commands |
|---|---|
| Planning | `/token-wise:plan-haiku`, `/token-wise:plan-sonnet`, `/token-wise:plan-opus` |
| PRD / specs | `/token-wise:prd-haiku`, `/token-wise:prd-sonnet`, `/token-wise:prd-opus` |
| CLAUDE.md | `/token-wise:claude-md-haiku`, `/token-wise:claude-md-sonnet`, `/token-wise:claude-md-opus` |
| README | `/token-wise:readme-haiku`, `/token-wise:readme-sonnet`, `/token-wise:readme-opus` |

## Auto-detection

Mention a text-heavy task in your prompt (e.g., "create a plan", "write a readme") and token-wise will detect it. A blocking prompt asks you to choose a model and suggests the right command. **You must select a model to continue** — your original prompt is held until you do.

After you choose, the skill runs on the selected model tier and automatically returns to your original session when done.

### Permission approval

The first time you run any token-wise skill, you'll see a permission approval prompt. Select **"Yes, and don't ask again"** to skip this prompt in future runs.

## Install

### Local development

```bash
claude --plugin-dir /path/to/token-wise
```

Or add to persistent plugin directories:

```bash
claude config set plugins.dirs '["~/path/to/token-wise"]'
```

### From source

```bash
git clone https://github.com/vivek-cactus/token-wise.git
cd token-wise
claude --plugin-dir .
```

## How it works

1. **Explicit invocation**: Type `/token-wise:skill-model` (e.g. `/token-wise:plan-sonnet`) to run immediately
2. **Auto-detection**: Mention a text task in chat and the hook detects it, shows model options, and blocks until you choose
3. **Background run**: The skill runs on the selected model tier
4. **Auto-return**: Output is written to disk and your session returns to the original model

## Output

Every skill writes its output to the project root:

- `CLAUDE.md` — project documentation
- `PLAN.md` — implementation or sprint plans
- `PRD.md` — product requirements
- `README.md` — project README

## Architecture

token-wise uses a **hook + skill system**:

- **Hook** (`detect_task.py`): Monitors your prompts for task keywords and intercepts text-heavy work
- **Skills** (`skills/`): Self-contained generators for each document type, running on the specified model tier
- **CLI integration**: Works seamlessly with Claude Code's native command system

## Contributing

Contributions welcome. Fork, branch, and open a PR. Skills are defined in `skills/` as self-contained SKILL.md files.

## License

MIT — see [LICENSE](./LICENSE)
