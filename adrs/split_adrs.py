#!/usr/bin/env python3
"""
Split adrs.md into individual ADR files.
Run from the directory containing adrs.md:
    python split_adrs.py
Output files will be written to ./adrs/ folder.
"""

import os
import re

INPUT_FILE = "adrs.md"
OUTPUT_DIR = "adrs"

SLUG_MAP = {
    "001": "monorepo",
    "002": "data-local-only",
    "003": "model-agnostic-control-plane",
    "004": "mcp-vs-cli",
    "005": "task-vs-agent",
    "006": "prompt-registry",
    "007": "approval-gate",
    "008": "observability",
    "009": "externalize-config",
    "010": "two-claude-md-pattern",
    "011": "react-harness-model",
}

def split_adrs(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as f:
        content = f.read()

    # Split on ADR headers
    blocks = re.split(r'(?=^## ADR-\d{3})', content, flags=re.MULTILINE)

    written = []
    for block in blocks:
        block = block.strip()
        if not block.startswith("## ADR-"):
            continue

        match = re.match(r'## ADR-(\d{3})', block)
        if not match:
            continue

        num = match.group(1)
        slug = SLUG_MAP.get(num, "untitled")
        filename = f"ADR-{num}-{slug}.md"
        filepath = os.path.join(output_dir, filename)

        # Clean up header from ## to #
        block = block.replace(f"## ADR-{num}", f"# ADR-{num}", 1)

        with open(filepath, "w") as f:
            f.write(block + "\n")

        written.append(filename)
        print(f"  wrote {filename}")

    print(f"\nDone — {len(written)} ADRs written to ./{output_dir}/")

if __name__ == "__main__":
    split_adrs(INPUT_FILE, OUTPUT_DIR)
