# Refining AI Agent & Copilot Environments: Lessons from Practice

This document summarizes key recommendations for refining AI agent/copilot environments and prompt engineering, inspired by the article "AIにコーディングを全任せした結果、ドメイン設計に辿り着いた話" (Zenn, 2026/04/20).

## 1. Clarify Domain Design Upfront
- Define domain concepts, boundaries, and naming conventions before starting AI-driven implementation.
- Document domain models and business logic separately from technical details.
- Use tools or prompts that facilitate domain-driven design (DDD) discussions and modeling.

## 2. Establish and Document Design Criteria
- Explicitly state design and commonality criteria in your instructions and prompt files.
- Add a section for “Design Principles & Judgement Criteria” to guide both AI and human contributors.

## 3. Layered AI Application
- Apply AI differently by code layer:
  - **Domain Layer:** Human-driven, AI-assisted (focus on correctness and consistency).
  - **Application Layer:** AI and human collaboration (semi-automated, with review).
  - **Infrastructure/Presentation:** AI-driven, with automated tests.

## 4. Modularize and Isolate Services
- Encourage code and prompt modularization by service/domain.
- Document how to split monorepos or large projects into smaller, independently managed units.

## 5. Feedback and Review Loops
- Review AI-generated code against domain models and design criteria, not just for correctness.
- Add checklists for reviewing naming, responsibility boundaries, and code reuse.

## 6. Version and Centralize Domain Knowledge
- Store domain models, vocabularies, and design decisions in versioned, accessible files.
- Reference these in prompt files and agent instructions.

## 7. Human-in-the-Loop for Meaningful Decisions
- Document which decisions require human input (e.g., business value, what to build, why).
- Make it clear in your process which steps are not to be automated.

## 8. Continuous Refinement
- Iterate on domain models and design criteria as the business evolves.
- Use feedback from implementation and review to update both domain documentation and prompt files.

---

*Reference: [AIにコーディングを全任せした結果、ドメイン設計に辿り着いた話](https://zenn.dev/tan_go238/articles/002437e923913c)*
