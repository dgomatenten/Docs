# AI Agent & Copilot Environment Configuration Guide

This guide summarizes best practices for configuring your development environment for GitHub Copilot, Copilot Chat, and AI agent-driven workflows, inspired by real-world AI-native development experiences.

## 1. Directory Structure Example

```
.github/
  doc_format/         # Document templates
  prompts/            # All prompt files (versioned, small, focused)
  rules/              # Coding/process rules
  skills/             # (Optional) Agent skills
  structures/         # Project and doc structure definitions
  task-format/        # Task templates for agents
  copilot-instructions.md  # Central Copilot/AI agent instructions
```

## 2. Best Practices

- **Keep files small:** Split large prompts/instructions into smaller, reusable files.
- **Version control everything:** All prompts, rules, and templates should be in git.
- **Centralize instructions:** Use a single `copilot-instructions.md` for Copilot/AI agent guidance.
- **Explicit referencing:** Reference only what’s needed in each prompt to avoid context overflow.
- **Iterate and review:** Regularly update prompts and instructions based on feedback and results.
- **Structured bug/issue tracking:** Use machine-readable formats (JSON, CSV) for bug reports if you want to automate analysis.

## 3. Documentation and Process

- Design your documentation structure so that AI agents can easily find and use the information they need.
- Align your documentation with your software architecture for easy cross-reference.
- Store all process knowledge, rules, and templates in the repository for transparency and reproducibility.

## 4. Prompt Engineering

- Avoid ad-hoc prompting in chat; always use versioned prompt files.
- When changes are needed, update the prompt file and rerun the process.
- Use review/feedback tickets to drive improvements and keep knowledge in the repo.

## 5. Testing and Quality

- Test coverage and test case extraction are critical—don’t rely solely on AI-generated tests.
- Maintain and improve test case templates and checklists as part of your `.github` structure.

## 6. Project Management

- Use simple TODO lists and burndown charts for small teams.
- For bug management, prefer structured formats (JSON, CSV) over markdown for easier aggregation and analysis.

## 7. For Copilot Chat/CLI

- Place all Copilot-related skills, instructions, and prompt templates under `.github/`.
- Use the `prompts/` folder for all prompt engineering work.
- Use `copilot-instructions.md` to document and refine your Copilot usage patterns and best practices.
- Optionally, use `skills/` for advanced Copilot Chat skills or workflows.

## 8. Example: Adding a New Prompt

1. Create a new file in `.github/prompts/` (e.g., `add-user-flow.md`).
2. Keep the prompt focused on a single task.
3. Reference only the necessary rules or templates.
4. Update `copilot-instructions.md` if this prompt introduces a new pattern or best practice.

## 9. Summary

- Use `.github/` as your AI agent and Copilot workspace.
- Organize by function: prompts, rules, skills, templates, and instructions.
- Keep everything small, explicit, and versioned.
- Centralize and document your Copilot/AI agent instructions for team-wide consistency and reproducibility.

---

*Inspired by: [設計書・コード・テストを全部AIに書かせて半年間開発してみたよ](https://zenn.dev/nttdata_tech/articles/8a010aff542625)*
