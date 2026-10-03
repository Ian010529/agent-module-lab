# Known next steps do not need the Agent Tool protocol

The user demonstrated the Slice 2 control-boundary transfer from the pinned `agents-from-scratch` reference into the Creator Outreach project.

They can reconstruct the main Tool Calling chain as:

`@tool → get_tools → bind_tools → LLM → tool_calls → tools_by_name → invoke → tool message → LLM`

and distinguish the model-selected Tool protocol from a workflow step whose next action is already known.

For the Slice 2 case where `CreatorReply + campaign_id` always requires a Campaign rules lookup, the user correctly concluded that the **entire Tool Calling loop should be removed** and the application should call the lookup function directly.

They also identified deterministic policy checks such as:

- allowed currency membership;
- required information missingness;
- numeric threshold comparisons;
- explicit enum / allowed-set membership.

## Evidence

The user passed the Lesson 0002 page gates, reconstructed the reference Tool Calling chain, corrected the transfer boundary for the Campaign lookup, and explicitly concluded: “整个tool loop删掉 直接调用函数执行即可”.

This demonstrates the understanding required to enter Own Design. It does **not** yet mean Tool Calling or Policy Gate is `PRACTICED`; practice requires implementation and verification in this project.
