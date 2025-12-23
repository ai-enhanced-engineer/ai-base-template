# Project Plan: [Project Name]

---
**Status**: Active
**Created**: [YYYY-MM-DD]
**Last Updated**: [YYYY-MM-DD]
**Current Phase**: Phase 1 - Context Research
---

## Overview

| Aspect | Details |
|--------|---------|
| **Project Goal** | [1 sentence describing end state] |
| **Target Users** | [Primary user personas] |
| **Success Criteria** | [How we measure success] |
| **Timeline** | [Estimated duration or target date] |
| **Team Size** | [Number of contributors] |

Example:
| Aspect | Details |
|--------|---------|
| **Project Goal** | Enable developers to capture, synthesize, and retrieve research findings efficiently |
| **Target Users** | Software engineers, technical leads, architects |
| **Success Criteria** | 50% reduction in research time, 80% of decisions documented |
| **Timeline** | 8 weeks to MVP, 4 weeks for enhancement phase |
| **Team Size** | 2 developers + 1 PM |

---

## Phase 1: Context Research

**Status**: [Not Started | In Progress | Complete | Blocked]
**Owner**: context-engineer
**Duration**: [Estimated time]

### Objectives

1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

Example:
1. Understand technical landscape for chosen domain
2. Identify best practices and anti-patterns
3. Create structured context for architecture planning

### Deliverables

- [ ] `context/` folder structure created
- [ ] `context/product/PRD.md` drafted (based on user input)
- [ ] `context/research/technology-comparison.md` completed
- [ ] `context/research/best-practices.md` completed
- [ ] `~/.claude/context/research/{project}-synthesis.md` written

### Success Criteria

- [ ] Research synthesis includes 5+ sources with evidence grades
- [ ] PRD has complete "Must-Have" user stories
- [ ] All claims in research docs are sourced
- [ ] User approves context structure and content

### Blockers & Risks

| Issue | Impact | Mitigation | Owner |
|-------|--------|------------|-------|
| [Blocker/risk] | High/Med/Low | [How to address] | [Who] |

Example:
| Issue | Impact | Mitigation | Owner |
|-------|--------|------------|-------|
| Insufficient user requirements | High | Schedule clarification meeting | PM |
| Technology rapidly evolving | Medium | Focus on stable core, flag experimental | context-engineer |

---

## Phase 2: Architecture Planning

**Status**: [Not Started | In Progress | Complete | Blocked]
**Owner**: project-architect
**Duration**: [Estimated time]

### Objectives

1. [Objective 1]
2. [Objective 2]

Example:
1. Make and document key architectural decisions
2. Define clear MVP scope with feature roadmap
3. Prepare template skeleton for implementation

### Deliverables

- [ ] `context/architecture/ADR.md` with 3-5 decisions
- [ ] `context/planning/PROJECT_PLAN.md` (this file) completed
- [ ] `pyproject.toml` updated with dependencies
- [ ] `README.md` customized for project
- [ ] `src/` folder structure created (if applicable)

### Success Criteria

- [ ] Each ADR follows standard format (Context/Decision/Consequences)
- [ ] MVP scope clearly separates Must/Should/Could/Won't
- [ ] Roadmap has at least 5 prioritized features
- [ ] User approves architecture and plan

### Dependencies

- **Requires**: Phase 1 complete (approved PRD and research)
- **Blocks**: Phase 3 (cannot start implementation without plan)

### Blockers & Risks

[Same table format as Phase 1]

---

## Phase 3: MVP Implementation

**Status**: [Not Started | In Progress | Complete | Blocked]
**Owner**: [domain-specialist - select based on project type]
**Duration**: [Estimated time]

### Objectives

1. Implement all "Must-Have" features
2. Create end-to-end working system
3. Establish testing and validation pipeline

### MVP Scope

#### Must-Have Features (In Scope)

| Feature | Description | Acceptance Criteria | Status |
|---------|-------------|---------------------|--------|
| [Feature 1] | [Brief description] | [How to test] | Not Started |
| [Feature 2] | [Brief description] | [How to test] | Not Started |
| [Feature 3] | [Brief description] | [How to test] | Not Started |

Example:
| Feature | Description | Acceptance Criteria | Status |
|---------|-------------|---------------------|--------|
| User Auth | Email/password login | User can register, login, logout | Not Started |
| Research Capture | Save web findings with metadata | User can add URL, extract content, save to DB | Not Started |
| Search | Full-text search of findings | User can search and get ranked results | Not Started |

#### Out of Scope (MVP)

**These features are intentionally excluded from MVP**:
- [Feature] - [Reason for exclusion]
- [Feature] - [Reason for exclusion]

Example:
- Social login (Google/GitHub) - Adds complexity without validating core value
- Real-time collaboration - Not needed for single-user validation
- Mobile app - Web-first approach, mobile later if needed

### Deliverables

- [ ] All Must-Have features implemented
- [ ] Unit tests for core functionality (>70% coverage)
- [ ] Integration tests for end-to-end flows
- [ ] Documentation updated (README, API docs)
- [ ] `just validate-branch` passes

### Success Criteria

- [ ] End-to-end user workflow completes without errors
- [ ] All acceptance criteria met for Must-Have features
- [ ] Test suite passes (`just test`)
- [ ] Type checking passes (`just type-check`)
- [ ] Linting passes (`just lint`)
- [ ] User validates MVP functionality

### Dependencies

- **Requires**: Phase 2 complete (approved architecture and plan)
- **Blocks**: Phase 4 (cannot enhance without working MVP)

### Blockers & Risks

[Same table format as Phase 1]

---

## Phase 4: Iterative Enhancement

**Status**: [Not Started | In Progress | Complete | Blocked]
**Owner**: [same domain-specialist from Phase 3]
**Duration**: [Estimated time or "Ongoing"]

### Objectives

1. Incrementally add features from roadmap
2. Incorporate user feedback
3. Maintain quality as system grows

### Feature Roadmap

Features prioritized using **MoSCoW**:
- **Must**: Critical for initial release
- **Should**: Important but not critical
- **Could**: Nice to have if time permits
- **Won't**: Out of scope for V1

| Priority | Feature | Description | Dependencies | Status |
|----------|---------|-------------|--------------|--------|
| Must | [Feature] | [Brief desc] | [Other features] | Not Started |
| Should | [Feature] | [Brief desc] | [Other features] | Not Started |
| Should | [Feature] | [Brief desc] | [Other features] | Not Started |
| Could | [Feature] | [Brief desc] | [Other features] | Not Started |
| Won't | [Feature] | [Brief desc] | - | Deferred |

Example:
| Priority | Feature | Description | Dependencies | Status |
|----------|---------|-------------|--------------|--------|
| Must | Social Login | Google/GitHub OAuth | User Auth | Not Started |
| Must | Export Results | Download research as Markdown/PDF | Search | Not Started |
| Should | Tagging System | Categorize findings by topic | Research Capture | Not Started |
| Should | Sharing | Share findings with team | User Auth | Not Started |
| Could | Browser Extension | Capture research from browser | API | Not Started |
| Won't | AI Summarization | Auto-summarize long articles | - | Deferred to V2 |

### Implementation Approach

**Per Feature**:
1. Review feature requirements and acceptance criteria
2. Update architecture if needed (new ADR)
3. Implement feature in isolated branch
4. Add tests (unit + integration)
5. Update documentation
6. Submit for user approval
7. Merge after approval

**Approval Gates**: User reviews each feature before next begins

### Success Criteria (Per Feature)

- [ ] Feature meets acceptance criteria from roadmap
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] No regression in existing functionality
- [ ] `just validate-branch` passes

### Dependencies

- **Requires**: Phase 3 complete (working MVP)
- **Enables**: Production release

### Blockers & Risks

[Same table format as Phase 1]

---

## Milestones

**High-level project checkpoints**:

| Milestone | Target Date | Criteria | Status |
|-----------|-------------|----------|--------|
| Phase 1 Complete | [YYYY-MM-DD] | Context approved | Not Started |
| Phase 2 Complete | [YYYY-MM-DD] | Architecture approved | Not Started |
| MVP Launch | [YYYY-MM-DD] | All Must-Haves working | Not Started |
| V1.0 Release | [YYYY-MM-DD] | All Should-Haves complete | Not Started |

---

## Technical Milestones

**Infrastructure and tooling setup**:

| Milestone | Description | Owner | Status |
|-----------|-------------|-------|--------|
| Dev Environment | Docker compose, local DB | [Name] | Not Started |
| CI/CD Pipeline | GitHub Actions, auto-deploy staging | [Name] | Not Started |
| Monitoring | Logging, error tracking, metrics | [Name] | Not Started |
| Production Deploy | Cloud deployment, custom domain | [Name] | Not Started |

---

## Metrics & KPIs

**How we measure progress and success**:

### Development Metrics

| Metric | Target | Current | Tracking Method |
|--------|--------|---------|-----------------|
| Test Coverage | >70% | 0% | pytest-cov |
| Type Coverage | >90% | 0% | mypy strict mode |
| Build Success Rate | >95% | N/A | GitHub Actions |

### Product Metrics (Post-Launch)

| Metric | Target | Current | Tracking Method |
|--------|--------|---------|-----------------|
| Active Users | 20/month | 0 | Analytics dashboard |
| Research Quality | 90% "helpful" | N/A | User survey |
| Time Savings | 50% reduction | N/A | Before/after comparison |

---

## Dependencies & Integrations

**External systems and services**:

| Dependency | Purpose | Status | Risk |
|------------|---------|--------|------|
| [Service] | [What it's for] | [Integrated/Pending] | High/Med/Low |

Example:
| Dependency | Purpose | Status | Risk |
|------------|---------|--------|------|
| OpenAI API | LLM for synthesis | Integrated | Low - stable API |
| PostgreSQL | Primary database | Integrated | Low - mature tech |
| OAuth Providers | Social login | Pending | Medium - config complexity |
| AWS S3 | File storage | Not started | Low - well-documented |

---

## Risk Register

**Ongoing risks and mitigations**:

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| [Risk description] | High/Med/Low | High/Med/Low | [How to address] | [Who] |

Example:
| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| Scope creep in MVP | Medium | High | Strict adherence to Must-Have list, defer to Phase 4 | PM |
| API cost exceeds budget | Low | Medium | Implement caching, rate limiting, cost alerts | Backend Dev |
| Key developer unavailable | Low | High | Documentation, knowledge sharing, pair programming | Team Lead |

---

## Change Log

**Track significant plan updates**:

| Date | Change | Reason | Author |
|------|--------|--------|--------|
| [YYYY-MM-DD] | Initial plan created | Project kickoff | [Name] |
| [YYYY-MM-DD] | Added Social Login to Should-Have | User feedback | [Name] |
| [YYYY-MM-DD] | Moved AI Summarization to Won't | Complexity vs. value | [Name] |

---

## Notes for AI Agents

### Phase Transitions

**Before starting each phase**:
1. Read all deliverables from previous phase
2. Validate dependencies are met
3. Confirm success criteria are clear and measurable
4. Check for blockers and flag to user

**After completing each phase**:
1. Mark all deliverables as complete
2. Update phase status to "Complete"
3. Prepare handoff summary for next phase
4. Request user approval before proceeding

### Roadmap Execution (Phase 4)

**When implementing features from roadmap**:
1. Work on highest priority (Must → Should → Could)
2. Check dependencies (implement prerequisites first)
3. Implement one feature at a time (don't parallelize)
4. Request approval after each feature before next

**If feature blocked**:
1. Mark status as "Blocked"
2. Document blocker in Blockers & Risks table
3. Move to next unblocked feature
4. Flag to user

### Updating This Plan

**When to update**:
- Feature status changes (Not Started → In Progress → Complete)
- New risks identified
- Priorities change
- Blockers encountered
- Milestones reached

**How to update**:
1. Update relevant table/section
2. Add entry to Change Log
3. Update "Last Updated" date at top
4. Notify user if significant change (scope, timeline)

---

## Quick Reference

### Current Sprint Focus
**[Brief description of current work]**

Example:
> Implementing Phase 3 MVP - Focus on Research Capture feature (US-002). Target: Complete by [date].

### Next 3 Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

### Blockers Needing Attention
- [Blocker 1] - Owner: [Name]
- [Blocker 2] - Owner: [Name]

### Upcoming Approvals
- [ ] [Approval 1] - Due: [date]
- [ ] [Approval 2] - Due: [date]
