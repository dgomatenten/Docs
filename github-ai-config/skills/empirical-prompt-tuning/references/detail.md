# Empirical Prompt Tuning – Details

## Example Requirements Checklist
1. [critical] The skill must generate a valid output for the main scenario.
2. The skill must handle at least one edge case.
3. The output must be reproducible by a different AI session.
4. All terms and steps must be explicitly defined.

## Example Evaluation Report Structure
- Output/result: <summary>
- Requirement fulfillment:
  - 1. [critical] ... ○/×/partial (reason)
  - 2. ...
- Unclear points: <list>
- Discretionary completions: <list>
- Retry count and reasons: <number, explanation>

## Example Scenario
**Scenario:** A user wants to generate a changelog using Conventional Commits for a new TypeScript library. The skill should provide the config, manifest, and workflow files needed for release automation.

## Example Iteration Log
| Iteration | New unclear points | Requirement achievement | Notes |
|-----------|-------------------|------------------------|-------|
| 1         | 3                 | 2/4                    | Initial draft |
| 2         | 1                 | 4/4                    | Fixed unclear config |
| 3         | 0                 | 4/4                    | All clear, reproducible |

## References
- See SKILL.md for workflow and template.
- [mizchi's original article](https://zenn.dev/mizchi/articles/empirical-prompt-tuning)
