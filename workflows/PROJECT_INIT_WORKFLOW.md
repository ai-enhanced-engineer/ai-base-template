# Project Initialization Workflow

> **Runtime**: Claude Code
> **Recommended Orchestrator**: Opus (for multi-agent coordination)
> **Sub-agents**: Sonnet or Haiku (for specialized tasks)

Transform this template into a project-specific system through agent-orchestrated phases with user approval gates.

## Overview

| Aspect | Description |
|--------|-------------|
| **Purpose** | Transform template into project-specific system |
| **Pattern** | Sequential agent orchestration with incremental complexity |
| **Approval** | User approval required at each phase gate |

## Agent Role Definitions

This workflow uses **abstract roles** instead of specific agent names for portability. During Phase 0, Claude Code discovers available specialists and maps them to these roles.

| Role | Capability | Phase | Example Agents |
|------|------------|-------|----------------|
| `research` | Web research, evidence synthesis, context gathering | 1 | context-engineer, researcher |
| `architecture` | ADRs, system design, MVP scoping | 2 | project-architect, ml-systems-architect |
| `implementation` | Code writing, testing, domain expertise | 3-4 | ai-engineer, backend-engineer, data-engineer, agentic-engineer |
| `review` | Test enforcement, code quality auditing | 3-4 | python-code-quality-auditor |

**Role Matching Keywords**:

| Role | Keywords in Agent Description |
|------|-------------------------------|
| research | research, context, synthesis, investigation, analysis |
| architecture | architect, design, planning, ADR, system, infrastructure |
| implementation | engineer, developer, implement, code, build |
| review | review, audit, quality, test, enforce, validate, check, gate |

**Note**: The `implementation` role supports **multiple specialists** - different agents can be assigned to different features based on domain expertise.

---

## Discovered Agents

*This section is updated in place during Phase 0.*

| Role | Selected Agent(s) | Source | Status |
|------|-------------------|--------|--------|
| research | [pending discovery] | - | ⏳ |
| architecture | [pending discovery] | - | ⏳ |
| implementation | [pending discovery] | - | ⏳ |
| review | [pending discovery] | - | ⏳ |

---

## Phase 0: Agent Discovery

Before starting the workflow, Claude Code discovers available specialists and maps them to roles.

**Actions**:
1. Scan for agents at:
   - Project level: `.claude/agents/*.md`
   - User level: `~/.claude/agents/*.md`
2. Read agent descriptions and match to roles using keywords
3. Present candidates to user for approval
4. Update "Discovered Agents" section above with selections

**User Approval**:

Claude Code presents discovered agents:
```
Found specialists for this workflow:

research:       context-engineer (user) - "Web research and evidence synthesis"
architecture:   project-architect (user) - "ADRs and system design"
implementation: ai-engineer (user) - "RAG and LLM integration"
                backend-engineer (user) - "APIs and databases"
review:         python-code-quality-auditor (user) - "Code quality and test enforcement"

Approve these selections? [Y/n/modify]
```

**If No Matches Found**:

```
⚠️  WARNING: No specialist found for role [research].
    Workflow will proceed with generalist Claude Code.
    Consider creating a specialist agent for better results.
```

**After Discovery**:

Update the "Discovered Agents" table above, then proceed to Prerequisites.

---

## Inter-Phase Communication

Templates in `workflows/templates/` serve as **structured contracts** between phases:

| Template | Output Location | Produced By | Consumed By |
|----------|-----------------|-------------|-------------|
| `TEMPLATE-PRD.md` | `context/PRD.md` | `research` role (Phase 1) | `architecture` role (Phase 2) |
| `TEMPLATE-ADR.md` | `ADR.md` (root) | `architecture` role (Phase 2) | `implementation` role (Phase 3) |
| `TEMPLATE-PROJECT-PLAN.md` | `context/PROJECT_PLAN.md` | `architecture` role (Phase 2) | `implementation` role (Phase 3-4) |

Templates remain in `workflows/templates/` as reusable scaffolds.

**Why templates matter:**
- **Predictable handoffs**: Each phase knows exactly what format to expect
- **Agent independence**: Agents don't need to negotiate formats
- **Human readability**: User can review outputs at each approval gate

---

## Prerequisites

Before running this workflow:

1. **Fill out seed documents** in `context/`:
   - `context/PRODUCT.md` - Product/business perspective (what & why)
   - `context/ENGINEERING.md` - Technical perspective (how & constraints)

2. **Run Phase 0**: Discover and confirm available specialists (or accept generalist fallback)

3. **Support files** in `workflows/`:
   - Templates for agent outputs
   - Agent specifications

---

## Phase 1: Context Research

**Role**: `research`
**Agent**: *[See Discovered Agents table]*

**Input**:
- `context/PRODUCT.md` - User-provided product seed
- `context/ENGINEERING.md` - User-provided engineering seed

**Actions**:
1. Read user-provided seeds
2. Research technologies, patterns, best practices
3. Grade evidence quality (High/Medium/Low confidence)
4. Expand seeds into full PRD using `workflows/templates/TEMPLATE-PRD.md`
5. Synthesize findings into structured document

**Output**:
- `context/PRD.md` - Expanded PRD based on product seed
- `context/RESEARCH_SYNTHESIS.md` - Research synthesis

**Success Criteria**: Research synthesis with sourced, graded claims

### [APPROVAL GATE 1]

User reviews:
- Expanded PRD in `context/PRD.md`
- Research synthesis document

**Options**:
- ✅ **Approve** - Proceed to Phase 2
- 🔄 **Request more research** - Specify areas needing deeper investigation
- ✏️ **Modify scope** - Adjust seeds and re-run

---

## Phase 2: Architecture Planning

**Role**: `architecture`
**Agent**: *[See Discovered Agents table]*

**Input**:
- `context/PRD.md` - Expanded PRD from Phase 1
- Research synthesis from Phase 1
- `context/ENGINEERING.md` - Technical preferences
- Template skeleton (pyproject.toml, ADR.md, README.md, src/)

**Actions**:
1. Create ADRs using `workflows/templates/TEMPLATE-ADR.md`
2. Define MVP scope using MoSCoW prioritization
3. Plan incremental feature roadmap using `workflows/templates/TEMPLATE-PROJECT-PLAN.md`
4. Customize template (pyproject.toml, README.md)

**Output**:
- `ADR.md` - Overwritten with project-specific decisions
- `context/PROJECT_PLAN.md` - MVP scope + feature roadmap

**Success Criteria**: Clear MVP definition, actionable roadmap

### [APPROVAL GATE 2]

User reviews:
- Architecture decisions in `ADR.md`
- MVP scope and feature roadmap in `context/PROJECT_PLAN.md`

**Options**:
- ✅ **Approve** - Proceed to Phase 3
- 🔧 **Adjust scope** - Modify MVP boundaries
- 📊 **Change priorities** - Reorder feature roadmap

---

## Phase 3: MVP Implementation

**Roles**: `implementation` + `review`
**Agents**: *[See Discovered Agents table - may use multiple specialists]*

Phase 3 uses a structured **Implement → Review → Fix** loop for each deliverable to enforce test creation and code quality.

Select implementation agent based on project type:

| Project Type | Recommended Specialty |
|--------------|----------------------|
| RAG, embeddings, LLM integration | AI/ML specialist |
| APIs, databases, DDD | Backend specialist |
| Autonomous agents | Agentic specialist |
| ETL, data pipelines | Data specialist |

**Input**:
- Approved `ADR.md` and `context/PROJECT_PLAN.md` from Phase 2
- Customized template skeleton

---

### 3.1 Implementation Sub-phase

**Role**: `implementation`

**Actions**:
1. Implement one deliverable (feature/module) from PROJECT_PLAN.md
2. Write unit tests following naming convention: `test__<what>__<expected>`
3. Ensure tests are behavioral (test outcomes, not mocks)
4. Run `make test` locally to verify tests pass
5. Mark deliverable as "Ready for Review"

**Test Requirements**:
- Every new module must have corresponding unit tests
- Tests must follow naming convention from CLAUDE.md
- Minimum 80% coverage for new code
- No tautological tests (testing mocks, assignment, or nothing)

---

### 3.2 Review Sub-phase

**Role**: `review` (read-only)

**Actions**:
1. Verify tests exist for all new implementation files
2. Check test naming conventions (`test__<what>__<expected>`)
3. Detect tautological tests (testing mocks instead of behavior)
4. Verify coverage >= 80% for new code
5. Check for hallucinated packages (imports that don't exist)
6. Scan for security vulnerabilities (bare except, SQL injection)
7. Generate review report

**Blocking Criteria** (must fix before progression):
- [ ] Tests exist for all new implementation files
- [ ] Tests follow `test__<what>__<expected>` naming convention
- [ ] No tautological tests detected
- [ ] Coverage >= 80% for new code
- [ ] No hallucinated package imports
- [ ] No security vulnerabilities

**Review Report Format**:
```
## Test & Quality Review Report
**Deliverable**: [name]
**Status**: PASS | FAIL
**Coverage**: X% (required: 80%)
**Review Cycle**: N of 3

### Blocking Issues (must fix)
### Warnings (should fix)
### Passed Checks
### Remediation Required
```

---

### 3.3 Fix Sub-phase (If Review Fails)

**Role**: `implementation`

**Actions**:
1. Address each blocking issue from remediation list
2. Add missing tests if required
3. Fix tautological tests to be behavioral
4. Re-run `make test` locally
5. Return to 3.2 for re-review

**Loop Control**:
- Maximum **3 fix cycles** per deliverable
- If still failing after 3 cycles → **escalate to user**

---

### Validation Loop Diagram

```
PER DELIVERABLE:

┌─────────────────┐
│   IMPLEMENT     │ ← implementation role (code + tests)
└────────┬────────┘
         │
         v
┌─────────────────┐
│     REVIEW      │ ← review role (read-only)
└────────┬────────┘
         │
    ┌────┴────┐
    │  PASS?  │
    └────┬────┘
     Yes │ No
         │  │
    ┌────┘  └────┐
    v            v
┌──────┐    ┌──────┐
│ DONE │    │ FIX  │ ← implementation role
└──────┘    └──┬───┘
               │
          ┌────┴────┐
          │Cycle < 3│
          └────┬────┘
           Yes │ No
               │  │
         (back to REVIEW)  → ESCALATE TO USER
```

---

### Escalation Behavior

If a deliverable fails review 3 times:

1. **Generate Escalation Report** with:
   - All persistent blocking issues
   - Summary of attempted fixes across cycles
   - Recommendations for resolution

2. **Halt workflow** and present to user

3. **User Options**:
   - ⚠️ **Override** - Proceed anyway (document risk in PR)
   - 🔧 **Manual fix** - User addresses issues directly
   - ⏭️ **Descope** - Move feature to Phase 4 or backlog
   - ✂️ **Split** - Break into smaller deliverables

---

### Deliverable Tracking

| Deliverable | Status | Cycle | Blocking Issues | Owner |
|-------------|--------|-------|-----------------|-------|
| *[Feature 1]* | Implementing | 0 | - | implementation |
| *[Feature 2]* | In Review | 1 | Missing tests for X | review |
| *[Feature 3]* | Passed | 2 | - | - |

---

**Output**: Working MVP with tests (all deliverables passed review)

**Success Criteria**:
- All deliverables pass review
- `make validate-branch` passes
- Coverage >= 80% for new code

### [APPROVAL GATE 3]

User validates:
- MVP functionality (end-to-end)
- All deliverables passed review loop
- Test coverage meets requirements

**Options**:
- ✅ **Approve** - Proceed to Phase 4
- 🐛 **Request fixes** - Specify additional issues to address
- ✏️ **Adjust scope** - Modify MVP boundaries

---

## Phase 4: Iterative Enhancement

**Roles**: `implementation` + `review`
**Agents**: *[Same specialists from Phase 3, or different per feature]*

Phase 4 follows the same **Implement → Review → Fix** loop as Phase 3 for each feature in the roadmap.

**Input**:
- Working MVP from Phase 3
- Feature roadmap from `context/PROJECT_PLAN.md`

---

### 4.1 Feature Implementation

**Role**: `implementation`

**Actions**:
1. Select next feature from PROJECT_PLAN.md roadmap (by priority)
2. Implement feature with unit tests
3. Follow same test requirements as Phase 3:
   - Tests for all new modules
   - `test__<what>__<expected>` naming
   - 80% coverage for new code
   - Behavioral tests (not tautological)
4. Run `make test` locally
5. Mark feature as "Ready for Review"

---

### 4.2 Feature Review

**Role**: `review` (read-only)

**Actions**:
1. Run same validation as Phase 3.2 (tests, naming, coverage, quality)
2. Generate review report
3. If PASS → proceed to user approval
4. If FAIL → implementation agent fixes (max 3 cycles)

---

### 4.3 Feature Approval

### [APPROVAL GATE per feature]

After review passes, user validates:
- Feature functionality
- Review report shows PASS
- Integration with existing MVP

**Options**:
- ✅ **Approve** - Add next feature from roadmap
- 🔄 **Request changes** - Modify current feature
- ⏭️ **Skip to next** - Move to next roadmap item
- 🛑 **Stop** - End enhancement phase

---

**Output**: Enhanced system with additional features

**Success Criteria**:
- Each feature passes review loop
- `make validate-branch` passes
- Coverage maintained >= 80%

---

## Folder Structure

```
project-root/
├── context/                      # User seeds + workflow outputs
│   ├── README.md                 # Instructions for seeds
│   ├── PRODUCT.md                # User seed: product/business perspective
│   ├── ENGINEERING.md            # User seed: technical perspective
│   ├── PRD.md                    # Phase 1 output: expanded PRD
│   └── PROJECT_PLAN.md           # Phase 2 output: MVP scope + roadmap
├── workflows/                    # Workflow support files
│   ├── PROJECT_INIT_WORKFLOW.md  # This file
│   ├── QUICK-START.md            # Step-by-step guide
│   ├── README.md                 # Template docs
│   └── templates/                # Output templates
│       ├── TEMPLATE-PRD.md
│       ├── TEMPLATE-ADR.md
│       └── TEMPLATE-PROJECT-PLAN.md
├── ADR.md                        # Overwritten in Phase 2
└── src/                          # Implementation (Phase 3-4)
```

---

## Artifact Locations

| Artifact | Location | Created By |
|----------|----------|------------|
| User seeds | `context/PRODUCT.md`, `context/ENGINEERING.md` | **User** (before workflow) |
| Output templates | `workflows/templates/` | System (part of template) |
| Expanded PRD | `context/PRD.md` | `research` role (Phase 1) |
| Research synthesis | `context/RESEARCH_SYNTHESIS.md` | `research` role (Phase 1) |
| Architecture decisions | `ADR.md` | `architecture` role (Phase 2) |
| Project plan | `context/PROJECT_PLAN.md` | `architecture` role (Phase 2) |
| Implementation | `src/*.py` | `implementation` role (Phase 3-4) |

---

## Invocation Examples

**Step 0** - Fill out seeds:
```
Edit context/PRODUCT.md and context/ENGINEERING.md with your project details
```

**Phase 0** - Discover agents:
```
Run the project initialization workflow
```
Claude Code will scan for specialists, present them, and update this file.

**Phase 1** - Start context research:
```
Research context for this project using [discovered research agent]
```

**Phase 2** - Plan architecture:
```
Plan architecture for this project using [discovered architecture agent]
```

**Phase 3** - Implement MVP:
```
Implement MVP using [discovered implementation agent(s)]
```

**Phase 4** - Add features:
```
Add [feature name] from the roadmap using [appropriate implementation agent]
```

---

## Template Usage

Templates in `workflows/templates/` define output formats. Agents use these to produce consistent documents.

### PRD Template → `context/PRD.md`

**Used by**: `research` role (Phase 1)

**Key sections**:
- Problem Statement (from user seeds)
- Objectives (from success criteria)
- User Stories with acceptance criteria
- Constraints (from engineering seed)

### ADR Template → `ADR.md`

**Used by**: `architecture` role (Phase 2)

**Typical decisions**:
- ADR-001: Database choice
- ADR-002: Web framework
- ADR-003: Authentication
- ADR-004: Deployment
- ADR-005: State management

**Each ADR must have**: Context, Decision, Consequences, Alternatives

### Project Plan Template → `context/PROJECT_PLAN.md`

**Used by**: `architecture` role (Phase 2)

**Key sections**:
- Overview table with project details
- Phase status tracking
- MVP Scope (Must-Have features only)
- Feature Roadmap (Should/Could/Won't)

---

## Troubleshooting

### "Agent doesn't understand requirements"

**Cause**: User description too vague or context missing

**Fix**:
- Provide more specific problem statement
- Describe target users explicitly
- Include examples of desired functionality
- State constraints clearly

### "ADR doesn't match expectations"

**Cause**: PRD unclear or research missed key requirements

**Fix**:
- Review PRD - is problem statement clear?
- Provide direct feedback on what to change
- Edit ADR directly if easier

### "MVP scope too large/small"

**Cause**: Unclear boundaries in PRD or misaligned priorities

**Fix**:
- Review Must-Have vs. Should-Have in PRD
- Explicitly state what's NOT in MVP
- Adjust PROJECT_PLAN.md scope directly

### "Feature implementation diverges from plan"

**Cause**: Agent didn't read context or context unclear

**Fix**:
- Ensure ADR has "Accepted" status
- Ask agent to re-read specific context file
- Update context if requirements changed

---

## Agent Best Practices

1. **Read all context before acting**: Don't skip to implementation
2. **Ask clarifying questions**: Don't guess user intent
3. **One phase at a time**: Don't jump ahead
4. **Follow templates exactly**: Consistency matters
5. **Cross-reference liberally**: Link to sources and related docs

---

## Workflow Refinement

After each workflow execution, update this file to:

- [ ] Refine phase instructions based on learnings
- [ ] Add project-type-specific guidance
- [ ] Improve success criteria
- [ ] Document common issues and solutions

### Refinement Log

| Date | Change | Reason |
|------|--------|--------|
| *Initial* | Created workflow | Template adaptation needs |
| 2025-11-28 | Reorganized: context/ for seeds, workflows/ for support | Clearer separation of user inputs vs. system files |
| 2025-11-28 | Added Phase 0 agent discovery, abstract roles | Workflow portability - users may have different specialists |
| 2025-11-28 | Added `review` role with Implement → Review → Fix loop | Enforce test creation and code quality before progression |
