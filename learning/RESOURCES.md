# AI Module Engineering Resources

## Current Slice 3 — Next Action Recommendation + Safe Reply Draft

### Authoritative project reference

- [Project reference: `reference/agents-from-scratch`](https://github.com/Ian010529/agent-module-lab/tree/main/reference/agents-from-scratch)

Pinned at commit `603fc7a4ac6119004f43894395e504a1fefcc6c0`. This remains the only business-development reference for the current Creator Outreach / Reply Copilot stage.

### Source-first trace for Slice 3

- [Pinned source: `src/email_assistant/prompts.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/prompts.py)

Use for: how the response agent receives background/preferences/instructions, how response behavior is constrained, and where the reference explicitly avoids some commitments.

- [Pinned source: `src/email_assistant/tools/default/email_tools.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/tools/default/email_tools.py)

Use for: the concrete distinction between producing text and executing the side-effectful `write_email` Tool.

- [Pinned source: `src/email_assistant/email_assistant_hitl.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/email_assistant_hitl.py)

Use for: how a model-selected `write_email` action is intercepted before execution; how accept/edit/ignore/response affect the path; and how application control remains outside the LLM.

- [Pinned source: `src/email_assistant/email_assistant.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/email_assistant.py)

Use only as needed to contrast the non-HITL tool loop with the HITL version.

### Current learning boundary

The lesson for Slice 3 must teach enough technical detail for the user to:

- separate deterministic control flow from language generation;
- separate draft creation from external side effects;
- trace the reference's `write_email` + HITL path;
- identify where ungrounded facts or unauthorized commitments could enter a generated reply;
- make the project's action/draft/HITL design themselves after the learning gate.

Do **not** pre-decide the project's action schema, draft schema, orchestration framework, or final HITL mechanism inside the lesson.

## Previous Slice 2 — Tool boundary + direct lookup

- `learning/lessons/0002-known-next-step-is-not-a-tool.html`
- `learning/reference/tool-calling-boundary.html`
- `docs/decisions/0002-campaign-rules-policy-gate.md`

## Reference staging

The repository's existing staging is authoritative:

- `agents-from-scratch`: current Creator Outreach / Reply Copilot.
- `gpt-researcher`: later Creator / Competitor Research Copilot.
- `vanna`: later Campaign Performance Analyst.
- `tau2-bench`: evaluation reference when the project reaches evaluation work.

Do not pull a later reference into Slice 3 because it contains a similarly named concept.

## Gaps intentionally left for Own Design

After the learning gate, the user must decide:

- the exact next-action output contract;
- the exact draft output contract;
- which PolicyDecision states produce a draft, clarification path, or human handoff;
- whether any part needs Agent Tool Calling or whether fixed workflow is sufficient;
- whether HITL is needed in this Slice and at what boundary.

These are intentionally not solved by the Technical Foundation lesson.
