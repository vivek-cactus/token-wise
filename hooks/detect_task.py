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
    "readme":    "README generation",
    "prd":       "PRD / spec writing",
}

MODEL_OPTIONS = [
    ("haiku",  "fastest & cheapest"),
    ("sonnet", "balanced"),
    ("opus",   "most powerful"),
]


def detect_task(prompt: str) -> str | None:
    prompt_lower = prompt.lower()
    for skill, patterns in TASK_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, prompt_lower):
                return skill
    return None


def format_options(skill: str) -> str:
    lines = [f"  /token-wise:{skill}-{model}    ← {label}" for model, label in MODEL_OPTIONS]
    return "\n".join(lines)


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
    stop_message = (
        f"[token-wise] {label} detected.\n\n"
        f"Ask the user: \"token-wise: which model should handle this {label}?\"\n"
        f"Use \"token-wise\" as the label. Options:\n\n"
        f"{format_options(task)}\n"
    )

    print(json.dumps({"stopReason": stop_message}))
    sys.exit(0)


if __name__ == "__main__":
    main()
