# Session: Chief of Staff — Day 1
# Repo: ai/sessions/
# Date: 2026-05-13
# Participants: Sachin Kumar Anumula + Claude (Anthropic)

---

## Purpose of this session

Establish the foundation of Arya — a provider-agnostic personal OS for automating knowledge work — using a job search automation as the first use case. This session covers ecosystem understanding, architecture decisions, repo structure, and all ADRs before writing a single line of code.

---

## Key decisions made

### Ecosystem understanding
- Claude products are opinionated views on specific functions: Chat (reasoning), Code (developer productivity), Cowork (non-developer task automation)
- The Claude Platform is the engine — products are Anthropic's own cars built on top
- Arya is built on the platform API, not on any one product

### The personal OS vision
- Mobile-driven approval layer
- Execution on local workstation or cloud
- Provider-agnostic control plane — not loyal to Anthropic or any vendor
- Git as the memory and portability layer
- Model switching is a config change, not a code change

### Job search as first use case
- Problem: LinkedIn is a firehose — most postings are noise or ghost jobs
- Goal: Build a funnel that filters → scores → surfaces for mobile approval → tailors → applies
- Connection layer: Check LinkedIn CSV for 1st/2nd degree bridges before applying
- Personal outreach (text/call) is a valid channel — system surfaces talking points
- Notion as the workflow database — already familiar, free tier sufficient, mobile-friendly

### Tooling
- Notion: MCP for reads/writes
- LinkedIn CSV: processed locally via CLI, never uploaded to AI servers
- Claude Project: Job Search OS — system prompt + resume as knowledge
- Claude Code: daily driver for building Arya

### Repo structure
- `arya/` — execution repo (was cos)
- `ai/` — thinking repo (was personal-os-notes), critical reasoning on building scalable AI

---

## Arya folder structure (locked)

```
arya/
  CLAUDE.md                  # constitutional document — draft next
  adrs/                      # architecture decision records
  agents/                    # agentic workflows (phase 1+)
  automations/
    job-search/              # first automation — phase 0
  core/
    approval/                # mobile webhook
    cli/                     # shared CLI utilities
    llm/                     # model router (LiteLLM)
    mcp/                     # MCP server configs
    memory/                  # local data store
    observability/           # structured run logs
  data/                      # gitignored — personal data never hits git
  evals/                     # placeholder — not built yet
  infra/                     # config, secrets, scheduler, docker
  prompts/                   # prompt registry — first class artifacts
  ecosystem/
    providers/
      anthropic/             # empty until provider config needed
```

---

## ADR index

| ADR | Decision |
|---|---|
| 001 | Mono repo for Arya |
| 002 | Personal data never leaves local machine |
| 003 | Model-agnostic control plane |
| 004 | MCP for external data, CLI for owned logic |
| 005 | Automated task vs agent decision criteria |
| 006 | Prompt registry as first-class artifact |
| 007 | Approval gate before every irreversible action |
| 008 | Observability on every run |
| 009 | All config externalized |
| 010 | Two-CLAUDE.md pattern |
| 011 | ReAct as the harness mental model |

Full ADR text in `arya/adrs/` — split via `split_adrs.py`

---

## Job search system prompt

File: `arya/prompts/job-search-system-prompt.md`
Already drafted. Contains:
- Sachin's profile snapshot
- Hard filters (auto-disqualify)
- Soft scoring rubric (1–10)
- Structured output format
- Connection check logic (placeholder until LinkedIn CSV processed)
- Tailoring hook per scored job

---

## Profile snapshot (for CLAUDE.md)

- **Name:** Sachin Kumar Anumula
- **Location:** Dallas Metro, TX
- **Status:** Green Card — no sponsorship required
- **Experience:** 17+ years enterprise engineering
- **Certifications:** AWS, Azure, GCP Solutions Architect, CKA, Neo4j, SAFe
- **Target roles:** Principal Architect, Staff Architect, VP/Director Engineering, Enterprise/Solutions Architect, CTO (scale-up), Technical Advisor
- **Work preference:** Hybrid (1–3 days in office)
- **Comp floor:** $180,000 base — hard filter, no exceptions
- **Domain sweet spots:** Healthcare, Fintech, Logistics, Large-scale Platform Engineering, AI/ML infrastructure
- **Recent:** Principal Architect at McKesson ($90B revenue platform), Engineering Lead at JPMC ($4.2T asset bank)

---

## What was NOT done yet (next session)

- [ ] Draft `arya/CLAUDE.md` — constitutional document
- [ ] Set up VSCode with recommended extensions and settings
- [ ] Set up Claude Project "Job Search OS" in claude.ai
- [ ] Process LinkedIn connections CSV locally via script
- [ ] Build Notion database schema
- [ ] Write `automations/job-search/CLAUDE.md`
- [ ] Write `split_adrs.py` output into `arya/adrs/`
- [ ] Run first 3 LinkedIn jobs through the funnel

---

## Naming

| Name | What it is |
|---|---|
| Arya | The personal OS / execution repo |
| ai | The thinking repo — critical reasoning on building scalable AI |

---

## Principles established (not yet ADRs)

- Fast over perfect — iterate in phases, earn complexity
- Own the control plane — never let a vendor own your memory, scheduling, or approval logic
- Externalize all config — always, no exceptions
- ADR first, code second — decisions are documented before implementation
- Personal data stays local — no exceptions regardless of convenience

---

*Session continues in VSCode. Next artifact: arya/CLAUDE.md*
