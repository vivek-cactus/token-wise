#!/usr/bin/env python3
"""
token-wise: UserPromptSubmit hook
Detects text-heavy task intent in free-form prompts and suggests the right
model-specific skill variant to save tokens.
"""

import json
import sys
import re

TASK_PATTERNS = {
    "claude-md": [
        r"\bclaude\.md\b",
        r"\bproject context\b",
        r"\bclaude memory\b",
        r"\bproject memory\b",
        r"\bgenerate.*context\b",
        r"\bwrite.*claude\b",
        r"\bupdate.*claude\.md\b",
        r"\bcreate.*claude\.md\b",
        r"\bset up claude\b",
    ],
    "plan": [
        r"\bcreate a plan\b",
        r"\bmake a plan\b",
        r"\bwrite a plan\b",
        r"\bplan for\b",
        r"\barchitecture.*plan\b",
        r"\bdesign.*plan\b",
        r"\bsprint.*plan\b",
    ],
    "readme": [
        r"\breadme\b",
        r"\bwrite.*readme\b",
        r"\bcreate.*readme\b",
        r"\bgenerate.*readme\b",
    ],
    "prd": [
        r"\bprd\b",
        r"\bproduct requirements\b",
        r"\brequirements doc\b",
        r"\bfeature spec\b",
        r"\bwrite.*spec\b",
    ],
}

SKILL_LABELS = {
    "claude-md": "CLAUDE.md generation",
    "plan":      "project planning",
    "readme":    "README update",
    "prd":       "PRD / spec writing",
}

MODEL_DESCRIPTIONS = {
    "claude-md": {
        "haiku":  "Fastest and most cost-efficient. Good for straightforward CLAUDE.md updates.",
        "sonnet": "Balanced quality and speed. Recommended for most CLAUDE.md tasks.",
        "opus":   "Highest quality and deepest reasoning. Best for complex or comprehensive CLAUDE.md generation.",
    },
    "plan": {
        "haiku":  "Fastest and most cost-efficient. Good for simple, well-defined plans.",
        "sonnet": "Balanced quality and speed. Recommended for most planning tasks.",
        "opus":   "Highest quality and deepest reasoning. Best for complex architectural plans.",
    },
    "readme": {
        "haiku":  "Fastest and most cost-efficient. Good for simple, well-defined README updates.",
        "sonnet": "Balanced quality and speed. Recommended for most README tasks.",
        "opus":   "Highest quality and deepest reasoning. Best for complex or comprehensive README rewrites.",
    },
    "prd": {
        "haiku":  "Fastest and most cost-efficient. Good for simple, well-defined specs.",
        "sonnet": "Balanced quality and speed. Recommended for most PRD tasks.",
        "opus":   "Highest quality and deepest reasoning. Best for complex product requirements.",
    },
}


def detect_task(prompt: str) -> str | None:
    prompt_lower = prompt.lower()
    for skill, patterns in TASK_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, prompt_lower):
                return skill
    return None


def main():
    try:
        data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = data.get("prompt", "")
    if not prompt:
        sys.exit(0)

    # Skip if already invoking a token-wise skill directly
    if prompt.strip().startswith("/token-wise:"):
        sys.exit(0)

    # Free-form prompt detection — suggest the right skill
    task = detect_task(prompt)
    if not task:
        sys.exit(0)

    label = SKILL_LABELS[task]
    descs = MODEL_DESCRIPTIONS[task]

    ask_params = {
        "questions": [{
            "question": f"token-wise: which model should handle this {label}?",
            "header": "token-wise",
            "multiSelect": False,
            "options": [
                {"label": "Haiku",  "description": descs["haiku"]},
                {"label": "Sonnet", "description": descs["sonnet"]},
                {"label": "Opus",   "description": descs["opus"]},
            ]
        }]
    }

    # Plain text stdout is added to Claude's context as hook output (per docs).
    # JSON {"additionalContext": ...} is not reliably received by Claude.
    print(
        f"[token-wise] {label} detected. Do NOT directly process this request.\n"
        f"Do NOT apply using-superpowers, brainstorming, or any other skill.\n"
        f"Do NOT generate your own AskUserQuestion parameters.\n\n"
        f"Your ONLY action: call AskUserQuestion with this exact JSON (copy verbatim):\n\n"
        f"{json.dumps(ask_params, indent=2)}\n\n"
        f"After the user selects, invoke /token-wise:{task}-<chosen_model_in_lowercase>"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
