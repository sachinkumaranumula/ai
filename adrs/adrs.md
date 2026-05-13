# Architecture Decision Records
# cos repo — /adrs/
# Generated from session: Chief of Staff — Day 1
# Format: Decision / Why / Consequences

---

## ADR-001: Mono Repo for cos

**Decision:**
`cos` is a single dedicated GitHub repository containing all automations, agents, core harness, prompts, evals, and infra config.

**Why:**
One person building a personal OS does not have team boundaries that justify repo isolation. Shared code (LLM router, Notion client, approval webhook) would be duplicated or over-engineered into packages in a multi-repo setup. A mono repo gives full system visibility in one `git log` and makes the evolution from task to agent to orchestrated system seamless.

**Consequences:**
- Folder discipline is mandatory — the repo will become a junk drawer without it
- A second repo `personal-os-notes` holds thinking, exploration, and pre-decision notes
- ADRs live in `cos/adrs/` not in `personal-os-notes` — they are binding, not exploratory

---

## ADR-002: Personal Data Never Leaves Local Machine

**Decision:**
All personal data (resume, LinkedIn CSV, processed derivatives) lives in `data/` which is permanently gitignored. No personal data is uploaded to any AI provider's servers or committed to any repository.

**Why:**
Claude Pro (consumer plan) does not offer Zero Data Retention (ZDR). ZDR requires Enterprise plan with a signed DPA. LinkedIn connections CSV contains names, titles, and companies of 500+ people who did not consent to being uploaded to an AI system. The risk is asymmetric — the cost of a data leak is high, the cost of local processing is zero.

**Consequences:**
- All scripts that process personal data run locally via CLI
- AI providers receive only sanitized derivatives — never raw personal data
- `data/` must be the first entry in `.gitignore` before any other file is committed
- This rule applies to all future automations, not just job search

---

## ADR-003: Model-Agnostic Control Plane

**Decision:**
The control plane — orchestration, memory, scheduling, approval flows, prompt registry — is owned entirely by the user and is not dependent on any single AI provider's infrastructure.

**Why:**
Tying the control plane to a vendor (Anthropic Routines, Managed Agents, etc.) creates switching cost that compounds over time. The models themselves are commoditizing. The durable investment is in the abstractions above the model — prompts, workflows, decision logic — not in any vendor's execution layer.

**Consequences:**
- All automation logic is written as provider-agnostic Python scripts
- Model calls go through `core/llm/` router — no automation calls a provider directly
- Swapping providers is a config change in `ecosystem/providers/` not a code change
- Vendor-specific tooling (Claude Code, MCP servers) is treated as an adapter, not a dependency

---

## ADR-004: MCP for External Data, CLI for Owned Logic

**Decision:**
When integrating with a data source or system you don't own (Notion, GitHub, calendar, email) — use MCP. When building logic you own (scoring, processing, orchestration, approval) — use CLI scripts.

**Why:**
MCP provides a structured, permissioned, auditable interface to external systems. It is standardized and swappable. CLI gives full control over logic that needs to evolve with the system. Mixing concerns — using CLI to scrape external systems, or MCP to run business logic — creates brittle integrations and unclear ownership.

**Consequences:**
- MCP server configs live in `core/mcp/`
- CLI utilities and base classes live in `core/cli/`
- Every automation's own `CLAUDE.md` must declare which MCPs it connects to and which CLIs it owns
- Before building any integration, the MCP vs CLI decision must be made explicitly and documented

---

## ADR-005: Automated Task vs Agent — Decision Criteria

**Decision:**
Default to an automated task. Graduate to an agent only when the goal requires runtime judgment, dynamic context, branching decisions, or human approval gates.

**Why:**
Agents are harder to debug, more expensive to run, and harder to trust than deterministic scripts. A task that can be expressed as a fixed sequence of steps with rule-based failure handling does not need an agent. Premature agentification adds complexity without adding value.

**Consequences:**
- Phase 0 job search workflows are tasks — fixed sequence, structured output
- Phase 1+ job search becomes an agent when discover → score → bridge → approve → tailor → apply requires runtime judgment
- The graduation from task to agent requires a corresponding eval suite in `evals/` before running unattended
- Decision criteria table lives in `adrs/ADR-005` and is referenced in root `CLAUDE.md`

| Dimension | Automated Task | Agent |
|---|---|---|
| Steps known upfront? | Yes — fixed sequence | No — discovered at runtime |
| Branching / decisions? | None or rule-based | Judgment required |
| Failure handling? | Retry or alert | Self-correct and reroute |
| Human in the loop? | No — runs unattended | Yes — approval gates |
| Context needed? | Static — known at build | Dynamic — fetched at run |
| Output type? | Predictable, structured | Variable, synthesized |
| Cost of wrong action? | Low — reversible | High — needs approval |

---

## ADR-006: Prompt Registry as First-Class Artifact

**Decision:**
All prompts — system prompts, scoring rubrics, outreach templates, agent instructions — live in `prompts/` at the repo root, versioned in git, referenced by name from automations and agents. Prompts are never hardcoded as strings in scripts.

**Why:**
Prompts are the primary interface between the system and the model. They need to be versioned, auditable, and independently swappable from the code that uses them. Hardcoded prompts make it impossible to run evals, compare prompt versions, or tune behavior without touching business logic.

**Consequences:**
- Every automation references a prompt file — it does not define its own prompt inline
- Prompt changes are atomic commits with clear messages
- Evals in `evals/` run against prompt versions — a prompt can be improved without changing code
- Provider-specific prompt tuning lives in `ecosystem/providers/{provider}/prompts/` not in `prompts/`

---

## ADR-007: Approval Gate Before Every Irreversible Action

**Decision:**
No automation or agent takes an irreversible action (send a message, submit an application, make an outreach) without explicit human approval through the mobile approval gate.

**Why:**
The cost of a false positive — applying to the wrong job, sending a poorly timed message — is reputational and not recoverable. The approval gate is not overhead; it is the control plane working as designed. Speed comes from reducing the friction of the approval decision, not from removing the decision.

**Consequences:**
- The mobile approval gate in `core/approval/` is a required dependency for any action that touches the outside world
- Scoring, filtering, tailoring, and drafting are pre-approval — they can run automatically
- Sending, submitting, and outreach are post-approval — they never run automatically
- The approval payload presented on mobile must be complete enough to decide in 30 seconds

---

## ADR-008: Observability on Every Run

**Decision:**
Every automation and agent run produces a structured log entry in `core/observability/` capturing what ran, what was decided, what was produced, and any errors.

**Why:**
Without observability the ReAct loop (Reason → Act → Observe → repeat) has no Observe step. Debugging an agent that did something unexpected requires knowing what it reasoned, what it acted on, and what it saw in response. Lightweight structured JSON logs are sufficient to start — they grow into proper tracing in phase 2.

**Consequences:**
- Every automation script imports the observability logger from `core/observability/`
- Log entries are append-only — never overwritten
- Logs stay local — they are in `data/` and gitignored
- In phase 2, logs feed into evals to measure automation quality over time

---

## ADR-009: All Config Externalized

**Decision:**
No configuration value — API keys, model names, Notion database IDs, webhook URLs, thresholds, prompt file paths — is hardcoded in any script. All config is externalized to `infra/` or environment variables.

**Why:**
Hardcoded config is the fastest path to a broken system when any external dependency changes. It also makes the system impossible to run in a different environment (local vs cloud) without code changes. Externalized config means the same code runs everywhere with different config.

**Consequences:**
- `infra/.env.example` is the canonical list of all required config values — committed to git
- `infra/.env` contains actual values — permanently gitignored
- Scripts read config via a single `core/config.py` loader — never via `os.environ` directly in business logic
- `ecosystem/providers/{provider}/` holds provider-specific config files — empty until needed, never hardcoded

---

## ADR-010: Two-CLAUDE.md Pattern

**Decision:**
The repo has a root `CLAUDE.md` that is the constitutional document for the entire system. Every automation and agent has its own `CLAUDE.md` that scopes instructions to that specific task.

**Why:**
A single root CLAUDE.md becomes unmanageable as the system grows. An automation-level CLAUDE.md gives any agent or Claude Code session the exact context it needs without reading the whole system. The root CLAUDE.md establishes global rules; the local CLAUDE.md establishes task-specific rules that inherit from root.

**Consequences:**
- Root `CLAUDE.md` covers: identity, repo map, global behavioral rules, provider contract, decision criteria references
- Local `CLAUDE.md` covers: what this automation does, which MCPs it uses, which CLIs it owns, what approvals it requires, what it must never do
- Any new automation or agent must have a `CLAUDE.md` before any code is written
- Local CLAUDE.md never contradicts root CLAUDE.md

---

## ADR-011: ReAct as the Harness Mental Model

**Decision:**
The `cos` harness is designed around the ReAct loop — Reason, Act, Observe, repeat. Every component maps to one of these phases and the harness is not complete unless all phases are covered.

**Why:**
ReAct is a proven mental model for agentic systems that prevents the two most common failure modes: acting without reasoning (automation that does the wrong thing confidently) and reasoning without observing (agents that don't learn from their actions).

**Consequences:**
- Reason → `core/llm/` + `prompts/`
- Act → `automations/` + `agents/` + `core/approval/`
- Observe → `core/observability/` + `core/memory/`
- A component that doesn't fit this model needs explicit justification before being added
- Evals in `evals/` measure the quality of the full loop, not individual steps

---

*All ADRs generated from session: Chief of Staff Day 1*
*Next ADR index: 012*
*When a new architectural decision is made — ADR first, code second.*
