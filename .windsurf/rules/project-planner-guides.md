---
trigger: manual
---

# Plan-Driven Execution

## Source of truth
- The `plans/` directory is the source of truth for scope, sequencing, and acceptance criteria.

## Primary execution plan
- Execute work by following `plans/8-implementation-roadmap.md`.
- Start at Phase 0 and complete tasks strictly in the listed order.
- Do not start a new task until the current task is complete.
- Do not skip any tasks.
- Follow the request and limit the scope to the plan if requested.

## Before starting any task
- Open and review `plans/8-implementation-roadmap.md`.
- Read any plan files in `plans/` that are referenced by the current phase/task.
- Confirm you understand the task’s expected outcome and any dependencies.

## While working
- Use the plan as the checklist. If the plan conflicts with other notes, the plan wins.
- If you discover missing prerequisites, blockers, or ambiguities:
  - Record them under the current task in the plan (with a short proposed resolution).
  - Do not reorder tasks or expand scope without updating the plan.

## After finishing a task
- Update `plans/8-implementation-roadmap.md` to mark the task as done.
- Add brief completion notes (what changed, where, and any follow-ups).
- Re-check the plan to identify the next task before doing anything else.
