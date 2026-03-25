# CLAUDE.md

## Summary

This repository follows a structured, phase-based workflow designed for effective collaboration.

The goal is to:
- Maintain a clear separation between planning, execution, and history
- Provide a predictable working environment for iterative development
- Enable safe, trackable, and reversible progress on complex projects

Claude should treat this repository as a controlled workspace with defined responsibilities for each file.

---

## Project Goals

This project should evolve from its starting state to the defined end state described in:

- `.claude/OVERVIEW.md`

This file contains:
- The full project architecture
- Layer definitions
- Phase breakdowns
- High-level tasks

Claude should use this as the long-term source of truth, but not as the active working document.

---

## File and Folder Structure

```
.claude/
  archive/
    prompts/         # Processed PROMPT.md entries
    phases/          # Completed phases
    progress/        # Archived progress logs
  OVERVIEW.md        # Full project overview and roadmap
  CURRENT_PHASE.md   # Active phase with granular tasks
  PROGRESS.md        # Periodic progress updates
  PROMPT.md          # Large prompt input (only read when referenced)

```

---

## Core Workflow

1. Read `.claude/CURRENT_PHASE.md` to understand the active work
2. Execute tasks incrementally
3. Update `.claude/CURRENT_PHASE.md` as tasks progress
4. Periodically append updates to `.claude/PROGRESS.md`
5. When a phase is complete:
   - Move contents of CURRENT_PHASE.md to `archive/phases/PHASE_[X].md`
   - Clear CURRENT_PHASE.md
6. Only begin the next phase after the current one is fully completed and archived

---

## File Definitions

### .claude/OVERVIEW.md

Purpose:
- Defines the complete project plan and architecture

Rules:
- Treated as read-only during normal execution
- Only updated when project direction changes are explicitly planned

---

### .claude/CURRENT_PHASE.md

Purpose:
- The authoritative source of truth for current work

Structure:
```
## Phase X: Name

### Objectives

### Tasks

### In Progress

### Blockers
```

Section Guidelines:

#### Objectives
- Short, high-level goals for the phase
- 3–5 concise bullets

#### Tasks
- Granular, actionable items
- Must be checkable (`- [ ]`)
- Should directly map to Objectives

#### In Progress
- Optional
- Short notes on active work
- No long explanations

#### Blockers
- Optional
- Clearly describe anything preventing progress

Rules:
- Do not duplicate content from OVERVIEW.md
- Do not use as a brainstorming document
- Keep concise and actionable

---

### .claude/PROMPT.md

Purpose:
- Holds large prompts or additional context that should not be inlined

Usage Rules:
- Only read when explicitly referenced in a main prompt
- After processing:
  1. Copy contents to `archive/prompts/PROMPT_[X].md`
  2. Increment X sequentially
  3. Clear PROMPT.md

---

### .claude/PROGRESS.md

Purpose:
- Tracks meaningful progress over time

Structure:
```
## Update: YYYY-MM-DD

### Completed

### In Progress

### Decisions

### Next
```

Section Guidelines:

#### Completed
- Tasks or milestones finished since last update

#### In Progress
- Current active work

#### Decisions
- Important choices made and why

#### Next
- Immediate upcoming work

Rules:
- Append-only until archived
- Focus on signal, not verbosity
- Avoid duplicating CURRENT_PHASE content

Archiving:
- If file exceeds ~30kb:
  - Move contents to `archive/progress/PROGRESS_[X].md`
  - Increment X sequentially
  - Clear PROGRESS.md

---

## Archive Structure

```
archive/
  prompts/
  phases/
  progress/
```

Purpose:
- Preserve history without polluting active context

Rules:
- Never modify archived files
- Always increment file indices sequentially

---

## Rules

### Execution

- Do not modify files outside the current phase unless required
- Prefer updating CURRENT_PHASE.md over creating new planning files
- Do not duplicate content across files

---

### File Rules

- OVERVIEW.md should not be updated unless project changes are planned
- CURRENT_PHASE.md is the source of truth for active work
- PROGRESS.md is append-only until archived

---

### Code Rules

- Code should be self-documenting with clear variable names
- Comments should be minimal and only explain complex logic
- Comments must be understandable without chat context
- Do not write comments that reference prompts or conversations

---

### General Rules

- Act as a collaborator, not just an executor
- Provide feedback if something is overengineered or hard to maintain
- Prefer editing existing files over creating new ones
- Only create new directories when necessary

---

## Definition of Done

A phase is complete when:
- All tasks in CURRENT_PHASE.md are checked off
- Objectives have been satisfied
- No active blockers remain
- A progress update has been recorded

After completion:
- Archive CURRENT_PHASE.md
- Clear it before starting the next phase
