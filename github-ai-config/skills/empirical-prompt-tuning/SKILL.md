---
name: empirical-prompt-tuning
description: Empirical prompt tuning workflow for reproducible, high-quality Copilot skills.
---
# Empirical Prompt Tuning for Copilot Skills

## Purpose
A workflow to iteratively refine Copilot skills (prompts) for clarity, reproducibility, and minimal ambiguity, inspired by [mizchi's empirical prompt tuning method](https://zenn.dev/mizchi/articles/empirical-prompt-tuning).

## Workflow
1. **Write the initial skill** as a markdown file with clear frontmatter (name, description).
2. **Prepare evaluation scenarios:**
   - 1 typical (median) scenario
   - 1–2 edge-case scenarios
3. **Define a requirements checklist:**
   - At least one `[critical]` item
   - Other important requirements
4. **Evaluation loop:**
   - Use a separate AI (or session) to execute the skill in each scenario.
   - Have the AI report:
     - Output/result summary
     - Requirement fulfillment (○/×/partial, with reasons)
     - Unclear points (list)
     - Discretionary completions (list)
     - Retry count and reasons
5. **Iterate:**
   - Fix one unclear point per iteration
   - Always use a new session for each test
   - Stop when two consecutive runs yield no new unclear points and all critical requirements are met
6. **Track metrics:**
   - Tool usage, time, requirement achievement

## Evaluation Template
```
You are an executor reading <skill name> for the first time.

## Target Prompt
<SKILL.md content or file path>

## Scenario
<Describe a typical or edge-case scenario>

## Requirements Checklist
1. [critical] <Minimum requirement>
2. <Other requirements>
...

## Task
1. Execute the scenario using the prompt.
2. At the end, report:
   - Output/result summary
   - Requirement fulfillment (○/×/partial, with reasons)
   - Unclear points (list)
   - Discretionary completions (list)
   - Retry count and reasons
```

## Example Directory Structure
```
.github/
  skills/
    empirical-prompt-tuning/
      SKILL.md
      references/
        detail.md
  settings.json
```

## Best Practices
- Always include at least one `[critical]` requirement.
- Use both typical and edge-case scenarios for evaluation.
- Keep references in separate files to avoid bloating the main skill file.
- Document unclear points and discretionary completions for each iteration.

## References
- [mizchi's article](https://zenn.dev/mizchi/articles/empirical-prompt-tuning)
- [empirical-prompt-tuning/SKILL.md example](https://github.com/mizchi/chezmoi-dotfiles/blob/main/dot_claude/skills/empirical-prompt-tuning/SKILL.md)
