# AX Workflow Experience — Workflow Model

## Purpose

This document defines a portable conceptual and data model for representing work performed collaboratively by a person and one or more agents. It operationalizes the **Workflow Experience** component of AX.

The model is not an agent runtime, scheduler, orchestration engine, chat UI or database. It describes the work state and the information an orchestrator should preserve so different interfaces and runtimes can participate without losing continuity.

## Design goals

1. **Outcome-first:** represent the requested outcome and its acceptance criteria before choosing tools or screens.
2. **Continuity:** preserve context, task state, decisions, evidence and the next useful action across turns and handoffs.
3. **Progressive disclosure:** ask for only the information needed to make the next safe decision.
4. **Adaptive planning:** allow the plan to change when evidence, constraints or blockers change.
5. **Human agency:** make approvals, delegated authority, pause and cancellation explicit.
6. **Observability:** distinguish planned, attempted, executed, verified and accepted work.
7. **Portability:** keep workflow state independent of a vendor-specific chat transcript or orchestration framework.
8. **Recoverability:** checkpoints and event history should support resumption after interruption.

## Core objects

| Object | Purpose |
|---|---|
| Workflow | The complete piece of work, its goal, constraints, state and acceptance criteria |
| Task | A bounded unit of work with dependencies, owner, status and outputs |
| Skill invocation | A request to use a versioned specialist capability under a defined contract |
| Approval | A human decision required before a consequential or restricted action |
| Artifact | A file or other deliverable produced during the workflow |
| Evidence | A source, observation or execution record supporting a finding |
| Event | An append-only record of a material state change or action |
| Checkpoint | A resumable snapshot of current state and the next action |

A workflow may contain many tasks and invocations. A Skill may be invoked by multiple workflows. Do not embed the full Skill methodology in the workflow record.

## Workflow lifecycle

The following statuses describe the workflow as a whole:

- `draft`: an initial request has been captured but not yet clarified.
- `intake`: the agent is resolving material ambiguity or collecting required inputs.
- `ready`: goal, constraints and success criteria are sufficient to begin.
- `running`: one or more tasks are actively progressing.
- `waiting_for_user`: a decision or missing input is required from the requester.
- `waiting_for_approval`: a permission or approval is required before an action.
- `blocked`: a dependency, capability or external condition prevents progress.
- `in_review`: work is ready for human or designated quality review.
- `completed`: acceptance criteria have been met and the result has been accepted or explicitly closed under the workflow's policy.
- `failed`: the workflow cannot proceed after its permitted recovery strategy.
- `cancelled`: the requester or authorized operator stopped the workflow.

Task statuses are narrower: `pending`, `ready`, `running`, `waiting`, `blocked`, `succeeded`, `failed`, `skipped`, `cancelled`.

A task can succeed while the workflow remains in progress. A workflow must not be marked completed merely because the final Skill returned successfully; outputs must be checked against the workflow's acceptance criteria.

## Typical state transitions

```text
draft -> intake -> ready -> running -> in_review -> completed
                     ^         |  \
                     |         |   -> waiting_for_user -> running
                     |         |   -> waiting_for_approval -> running
                     |         |   -> blocked -> running
                     |         |   -> failed
                     |         -> cancelled
                     \
                      (clarification changes scope)
```

This is a guide, not a rigid finite-state machine. The orchestrator validates transitions and records why a transition occurred. Recovery from `failed` should be an explicit retry or a new workflow, not an invisible status reset.

## Workflow record

The canonical workflow record should include:

- Stable workflow ID and protocol version.
- Human-readable title and goal.
- Requester and relevant participants.
- Context and references, not indiscriminate copies of all source material.
- Constraints: scope, deadline, risk, autonomy, source policy and output requirements.
- Observable success criteria.
- A plan composed of tasks, dependencies and assignments.
- Skill invocation references and their versions.
- Approvals and their decisions.
- Artifacts and evidence.
- Append-only event history.
- Checkpoint and next recommended action.

The JSON Schema in `schemas/ax-workflow.schema.json` defines the initial interoperable shape. It is intentionally extensible through explicit versioning rather than arbitrary vendor fields.

## Interaction loop: the workflow chat

The conversation is one possible control surface for the workflow, not the workflow's source of truth.

For each interaction, the orchestrator should:

1. Interpret the latest user intent against the existing workflow state.
2. Decide whether the goal, constraints or acceptance criteria changed.
3. Identify the next useful task or decision.
4. Check whether required information, capabilities and permissions exist.
5. Ask one focused question only when a material ambiguity blocks safe progress.
6. Otherwise proceed with the next reversible and authorized step.
7. Report meaningful progress, discoveries, blockers and handoffs.
8. Persist state changes and an event/checkpoint.
9. State the next action or completion condition.

Avoid dumping an entire project questionnaire into the chat. Gather information progressively. Do not ask the user to repeat context already present in the workflow.

## Planning and replanning

A plan is a working hypothesis, not a contract to follow blindly.

Replan when:
- new evidence invalidates an assumption;
- a dependency is unavailable;
- a task fails or returns partial output;
- the user changes the goal or constraints;
- the risk or approval requirement changes;
- the requested deliverable cannot be produced in the active runtime.

A replan must preserve completed work and explain material changes. Do not silently discard successful outputs.

## Human-agent coordination

Represent approvals as explicit records with:
- the proposed action;
- why it is needed;
- the scope and consequence;
- the requested permission;
- decision and decision-maker;
- timestamp and expiry where relevant.

An approval for one action is not blanket permission for unrelated actions. A Skill invocation does not grant permission to access accounts, transmit sensitive data, install packages or perform external writes.

The workflow should support pause, resume, correction, cancellation and escalation. The host agent must respect the actual permission model of its runtime.

## Evidence, artifacts and completion

Keep three concepts separate:

- **Evidence:** material supporting claims, calculations or decisions.
- **Artifact:** a deliverable such as a report, spreadsheet, chart or source file.
- **Acceptance:** the workflow-level judgment that the result satisfies the user's stated criteria.

Record provenance, timestamps, versions and limitations. An artifact reference does not prove its contents are correct. A completed execution does not prove the outcome is fit for purpose.

## Example: institutional equity research

A request to analyze a listed company may create tasks such as issuer identification, source collection, financial analysis, valuation, risk review, report generation and quality control.

The workflow owns the overall goal, progress, constraints and acceptance criteria. The equity-research Skill owns the specialist methodology and its calculations. The orchestrator decides when to invoke it. The runtime executes code if available. The interface presents progress and deliverables. The person resolves material assumptions and approves consequential actions.

See `examples/equity-research-workflow.json`.

## What this model deliberately does not prescribe

- A particular LLM, agent framework or multi-agent topology.
- A chat transcript format or visual component library.
- A database, event bus, scheduler or persistence vendor.
- A specific runtime, package manager or MCP implementation.
- Automatic autonomy or blanket user consent.

Those are implementation choices of the host system. The workflow data contract remains portable.
