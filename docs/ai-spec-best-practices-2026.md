# Best Practices for AI-Driven Specification Writing (2026) – Summary & Agent Setup Guide

## Article Summary

### 1. Specification as Code Seed & SSOT
- Modern specs are not just for human reading—they are the single source of truth (SSOT) and must be machine-readable for AI agents and tools.
- Avoid dumping unstructured info into long-context models; this leads to "consensus hallucination" (AI misunderstanding or inventing agreement).

### 2. Best Practice 1: Context ETL & Gravity Control
- Use a context ETL (Extract, Transform, Load) process to classify and prune information:
  - Level 1: Core Requirements (facts/constraints, e.g., DB schema, security, API specs)
  - Level 2: Supplementary Info (intent, interviews, history)
- Implement conflict resolution policies: AI should not resolve conflicts alone—output a Conflict Report and wait for human intervention.
- Attach metadata (date, TTL) to all info; regularly purge outdated knowledge.

### 3. Best Practice 2: LRS & Formal Invariants
- Enforce LLM-Readable Specs (LRS): Use strict formats like OpenAPI 3.1 or Protobuf for APIs/data models.
- Extract and define formal invariants (e.g., Stock ≥ Reserved) as logical expressions for system correctness.
- Use automation (e.g., n8n) to convert invariants into code (TypeScript Zod schemas, SQL CHECK constraints) and commit to Git.

### 4. Best Practice 3: Defensive Agentic Workflow & Git Sync
- Manage specs in Git, not wikis. All AI changes go through Pull Requests (PRs) for human review.
- Separate agent roles:
  - Agent A (PM): Drafts from business requirements.
  - Agent B (Engineer): Critiques for conflicts, fills gaps.
  - Agent C (Feedback): Feeds back implementation issues to update SSOT.
- Use circuit breakers: If agents loop >3 times, output a Conflict Report and notify humans.
- Human approval (Oracle) triggers ADR (Architecture Decision Record) generation and Git commit.

### 5. Best Practice 4: FinOps & Cost Management
- Apply strict workflows only to critical features (Tier 1: full loop, Tier 2: partial, Tier 3: simple diff review) to control AI usage costs.

### 6. Executable Prompt Templates
- Provide role-specific prompts for each agent (PM, Engineer, QA) with clear instructions, conflict policies, and output formats.

## Agent Setup & Workflow Recommendations

### Agent Roles & Prompts
- **PM Agent**: Classifies input, drafts specs, outputs in strict formats (OpenAPI, etc.), never resolves conflicts alone.
- **Engineer Agent**: Reviews for conflicts, security, technical debt, and outputs feedback or commit messages.
- **QA Agent**: Extracts invariants, validates testability, outputs logical expressions and test formats.

### Workflow
1. **Draft**: PM Agent creates spec draft from requirements.
2. **Review**: Engineer Agent critiques, requests changes, or outputs commit messages.
3. **QA**: QA Agent extracts invariants, validates testability.
4. **Sync**: All changes go through Git PRs; human reviews diffs and approves.
5. **Feedback Loop**: Implementation issues are fed back to update the SSOT.
6. **Circuit Breaker**: If agents loop >3 times, output Conflict Report and notify human.
7. **ADR**: On approval, generate and commit an ADR summarizing the decision process.

### Directory & File Structure Example
```
.github/
  specs/                # Machine-readable specs (OpenAPI, Protobuf)
  invariants/           # Formal invariants (logic, Zod, SQL)
  prompts/              # Role-specific agent prompts
  adr/                  # Architecture Decision Records
  workflows/            # Agentic workflow definitions
  conflict-reports/     # Conflict reports for human review
```

### Key Policies
- All specs and invariants must be in strict, machine-readable formats.
- All agent actions are versioned and reviewed via Git PRs.
- Conflict resolution is always escalated to humans.
- Use metadata and TTL for all knowledge artifacts.
- Apply strictest workflows only to critical features for cost control.

---

*Based on: [AIに仕様書を書かせるベストプラクティス 2026](https://qiita.com/YushiYamamoto/items/484792459af3afcba1a8)*
