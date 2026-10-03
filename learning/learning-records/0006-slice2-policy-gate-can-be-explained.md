# Slice 2 direct lookup and policy gate can be explained

The user completed the Slice 2 Understanding Check for Campaign Rules direct lookup and the deterministic Policy Gate.

They demonstrated that:

- a known next step should stay in ordinary application code rather than reintroducing LLM tool-selection;
- CampaignRules is a validated, complete business-rule contract, while CreatorReply can be schema-valid yet still legitimately omit facts that the creator did not provide;
- final status priority is `outside_policy > human_review > missing_information > within_policy`, while all applicable reasons are retained so downstream handling does not lose diagnostic information;
- the current design should be revisited when the upstream CreatorReply schema can no longer represent required business facts, or when `campaign_id` / the next action is no longer known and the workflow genuinely needs model-driven action selection.

## Evidence

In the Understanding Check, the user explained the direct-function boundary, distinguished business-configuration failure from creator-side missing information, described the status precedence, and identified both an upstream-schema trigger and a workflow-control trigger for redesign.
