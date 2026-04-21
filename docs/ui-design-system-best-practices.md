# Best Practices for Building and Maintaining AI-Ready UI Design Systems

This document summarizes the best way to build, document, and maintain a UI design system for AI-assisted development, based on insights from the article "DESIGN.md + 壊れたら気づくハーネス" (Zenn, 2026/04/11).

## 1. Three-Layer Structure for Sustainable UI Design

### Layer 1: DESIGN.md (Principles & Quick Reference)
- Write a single DESIGN.md file as the entry point for all AI agents and developers.
- Include:
  - **Design principles** (e.g., semantic colors, accessibility, shadow usage)
  - **Quick reference** for common components (cards, buttons, inputs, etc.)
  - **Prohibited patterns** (e.g., forbidden Tailwind classes, anti-patterns)
- Keep it concise and always up-to-date. This file should be AI- and human-readable.

### Layer 2: Structured Specs (contracts/ & rules.json)
- Move component specs and prohibited rules from Markdown tables to structured JSON files:
  - `contracts/`: JSON specs for each component (variants, tokens, accessibility, rules)
  - `rules.json`: Registry of all prohibited patterns, with IDs and alternatives
- Make these files the single source of truth for both AI and automation tools.
- Keep Markdown explanations for onboarding, but treat JSON as canonical.

### Layer 3: Verification Harness (harness/)
- Implement scripts/tests to:
  - Check JSON schema validity and rule/component consistency
  - Detect drift between documentation and actual data (e.g., number of rules/components)
  - Run on every PR via CI (e.g., GitHub Actions)
- Add real-time hooks or scripts to catch violations as soon as files are saved/changed.

## 2. Step-by-Step for Your Project

1. **Start with DESIGN.md**: Move all design principles, quick references, and prohibited patterns here. Keep process instructions (e.g., for Claude) in a separate file.
2. **Convert rules/specs to JSON**: Gradually migrate tables/lists to structured files. Start with a few, expand as needed.
3. **Add verification**: Even a simple script to compare counts between DESIGN.md and JSON is valuable. Expand to full schema checks and CI as the system grows.

## 3. Key Principles
- **Single Source of Truth**: Specs and rules should live in structured, machine-readable files.
- **Automated Consistency Checks**: Always verify that docs and data match—never rely on manual updates alone.
- **AI-First Documentation**: Write docs so that both AI agents and humans can use them directly.
- **Continuous Maintenance**: Expect your design system to grow; invest early in automation to prevent drift and decay.

## 4. Example DESIGN.md Structure
```
# DESIGN.md

## Principles
1. Use semantic colors (e.g., bg-primary-500)
2. Limit shadow to sm–md except for modals
3. Default to WCAG 2.1 AA accessibility

## Quick Reference
Card: bg-white rounded-xl border border-slate-200 p-6 shadow-sm
Button: inline-flex items-center justify-center h-10 px-4 bg-primary-500 text-white rounded-lg
Input: w-full px-3 py-2 border border-slate-300 rounded-lg

## Prohibited Patterns
- text-black → text-slate-900
- shadow-lg → shadow-sm
- border-t-4 → border border-slate-200
```

## 5. References
- [Original Article (Zenn)](https://zenn.dev/tsubotax/articles/7f0d3693f70e2f)
- [melta UI OSS](https://github.com/tsubotax/melta-ui)

---

*Quality is determined not just by good specs, but by robust verification and maintenance systems.*
