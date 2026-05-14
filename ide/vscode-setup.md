# VSCode Setup — Arya Development Environment
# Save this file to ai/sessions/vscode-setup.md

---

## Extensions

### Tier 1 — Install first, non-negotiable

| Extension | ID | Why |
|---|---|---|
| Claude Code | `anthropic.claude-code` | Native Claude Code in VSCode — inline diffs, plan mode, MCP support, subagents |
| Python | `ms-python.python` | Core Python support — Arya is Python |
| Pylance | `ms-python.vscode-pylance` | Fast type checking and intellisense for Python |
| GitLens | `eamodio.gitlens` | Git blame, history, heatmaps, AI commit messages via Anthropic API |
| GitHub Copilot | `github.copilot` | Inline completions — complements Claude Code, not a replacement |

### Tier 2 — Install second, high value

| Extension | ID | Why |
|---|---|---|
| Continue | `continue.continue` | Provider-agnostic chat in editor — swap Claude, GPT-4, local models. Aligns with ADR-003 |
| Ruff | `charliermarsh.ruff` | Fast Python linter and formatter — replaces flake8 + black |
| DotENV | `mikestead.dotenv` | Syntax highlight for .env files — you have a lot of config per ADR-009 |
| YAML | `redhat.vscode-yaml` | MCP server configs, infra configs are YAML |
| Markdown All in One | `yzhang.markdown-all-in-one` | CLAUDE.md and ADR editing — table of contents, formatting |
| Even Better TOML | `tamasfe.even-better-toml` | pyproject.toml support |

### Tier 3 — Add when needed

| Extension | ID | Why |
|---|---|---|
| Docker | `ms-azuretools.vscode-docker` | When infra/docker is built out |
| REST Client | `humao.rest-client` | Test approval webhooks and MCP endpoints without Postman |
| Thunder Client | `rangav.vscode-thunder-client` | Lightweight API testing — alternative to REST Client |
| JSON crack | `aykutsarac.jsoncrack-vscode` | Visualize complex JSON — observability logs |

---

## settings.json

Add to your workspace `.vscode/settings.json` inside both `arya/` and `ai/` repos.

```json
{
  // Python
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.typeCheckingMode": "basic",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },

  // Editor
  "editor.fontSize": 14,
  "editor.tabSize": 2,
  "editor.rulers": [88],
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,
  "editor.minimap.enabled": false,
  "editor.wordWrap": "on",
  "editor.formatOnSave": true,

  // Files
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/*.pyc": true,
    "**/.ruff_cache": true
  },
  "files.watcherExclude": {
    "**/data/**": true
  },

  // Git
  "git.autofetch": true,
  "git.confirmSync": false,
  "gitlens.ai.provider": "anthropic",

  // Markdown
  "[markdown]": {
    "editor.wordWrap": "on",
    "editor.quickSuggestions": {
      "other": "on"
    }
  },

  // Terminal
  "terminal.integrated.defaultProfile.osx": "zsh",
  "terminal.integrated.fontSize": 13,

  // Claude Code
  "claudeCode.autoApproveTools": false,

  // Explorer
  "explorer.fileNesting.enabled": true,
  "explorer.fileNesting.patterns": {
    "CLAUDE.md": "*.md",
    ".env.example": ".env,.env.*",
    "pyproject.toml": "ruff.toml,setup.py,setup.cfg,requirements*.txt"
  }
}
```

---

## extensions.json

Save to `.vscode/extensions.json` in both repos — VSCode will prompt anyone (including future you) to install these on repo open.

```json
{
  "recommendations": [
    "anthropic.claude-code",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "eamodio.gitlens",
    "github.copilot",
    "continue.continue",
    "charliermarsh.ruff",
    "mikestead.dotenv",
    "redhat.vscode-yaml",
    "yzhang.markdown-all-in-one",
    "tamasfe.even-better-toml"
  ]
}
```

---

## Python environment setup

Run once in `arya/` root before opening VSCode:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Mac/Linux
# .venv\Scripts\activate       # Windows

# Install base deps
pip install --upgrade pip
pip install ruff pytest python-dotenv httpx

# Freeze
pip freeze > requirements.txt
```

Add `.venv/` to `.gitignore` — it's never committed.

---

## .gitignore — arya/ (starter)

```
# Personal data — ADR-002, non-negotiable
data/

# Python
.venv/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/

# Env / secrets — ADR-009
.env
.env.*
!.env.example

# VSCode local
.vscode/settings.json    # workspace settings are committed
# only user-specific overrides excluded

# OS
.DS_Store
```

---

## Keyboard shortcuts worth knowing

| Shortcut (Mac) | Action |
|---|---|
| `Cmd+Shift+P` | Command palette |
| `Cmd+I` | Claude Code inline edit |
| `Cmd+Shift+I` | Open Claude Code panel |
| `Cmd+N` (in Claude panel) | New Claude conversation |
| `Ctrl+\`` | Toggle terminal |
| `Cmd+Shift+G` | Git panel |

---

*Next step: Open arya/ in VSCode, install extensions, then draft CLAUDE.md*
