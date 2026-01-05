---
trigger: always_on
---

# Plan-Driven Execution (PRs merged into dev/v1 must equal the plan)

## Source of truth
- `plans/` is the source of truth for scope, sequencing, and acceptance criteria.
- `plans/8-implementation-roadmap.md` is the primary checklist that defines “done”.

## Primary execution plan
- Execute work by following `plans/8-implementation-roadmap.md`.
- Start at Phase 0 and complete tasks strictly in the listed order.
- Do not start a new task until the current task is complete.
- Do not skip tasks. Do not expand scope beyond what the plan specifies (unless the plan is updated).

## Before starting any task
- Open and review `plans/8-implementation-roadmap.md` (current phase + current task).
- Read any plan files referenced by the current task.
- Confirm expected outcome, acceptance criteria, and dependencies.
- Create a new branch for the task (one task = one PR).

## While working
- Use the plan as the checklist. If something conflicts, the plan wins.
- If you discover missing prerequisites, blockers, or ambiguities:
  - Add a note under the current task in `plans/8-implementation-roadmap.md` with the proposed resolution.
  - Do not reorder tasks or expand scope without updating the plan first.
- Commit on meaningful milestones.
- Push to the remote repository.

## PR requirements (to guarantee dev/v1 ends up complete)
- Every task must produce exactly one PR targeting `dev/v1`.
- PR title must reference the exact task identifier/name from the plan.
- PR description must include:
  - Task link/quote from `plans/8-implementation-roadmap.md`
  - Acceptance criteria checklist copied from the plan (or a short “how verified” list if none exists)
  - What changed + where (files/areas)
  - Test/verification performed
  - Any follow-ups or known limitations (must be reflected in the plan if they matter)

## Creating the PR (always target dev/v1)
- After finishing the task and updating the plan (mark task as done + completion notes), create the PR:
  - `gh pr create --base dev/v1 --head <branch> --title "<plan task id>: <task name>" --body "<filled template>"`

## Merge gate (do not merge unless true)
- The PR must satisfy the task acceptance criteria as written in the plan.
- CI must be green (or explicitly waived with documented reason in PR + plan).
- The plan must be updated in the same PR:
  - Task marked as done
  - Completion notes added

## After merging
- Re-open `plans/8-implementation-roadmap.md`.
- Identify the next not-done task.
- Start the next task and repeat.

## Completion condition (what “we will have what we want” means)
- When all tasks in `plans/8-implementation-roadmap.md` are marked done and merged into `dev/v1`,
  `dev/v1` is considered complete and aligned with the intended scope.
