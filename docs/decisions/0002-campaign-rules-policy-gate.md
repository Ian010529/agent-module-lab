# Campaign rules direct lookup and deterministic policy gate

## Decision

Slice 2 treats `CreatorReply` as a stable upstream contract and does not reopen the Slice 1 extraction schema.

For a known `campaign_id`, the workflow performs a direct application call rather than exposing Campaign lookup as an Agent Tool:

`CreatorReply + campaign_id → lookup_campaign_rules → CampaignRules → evaluate_policy → PolicyDecision`

The v1 `CampaignRules` contract contains only:

- `campaign_id`
- `max_budget`
- `currency`
- `latest_delivery_date`

Campaign configuration must be complete before entering the policy gate. Missing or invalid Campaign rules fail at the lookup boundary; `missing_information` is reserved for missing CreatorReply facts.

The v1 decision states are:

- `within_policy`
- `outside_policy`
- `missing_information`
- `human_review`

When multiple conditions apply, status priority is:

`outside_policy > human_review > missing_information > within_policy`

All applicable reason codes are retained.

## Rule boundary

Deterministic code handles:

- explicit currency comparison;
- exact/ranged budget comparisons where the result is unambiguous;
- explicit delivery dates/ranges versus the campaign deadline;
- missing structured facts.

The gate does not invent structure from `Quote.conditions`. Natural-language conditions, multiple quotes, ambiguous quote bases, approximate/range cases that cross a threshold, and other facts that cannot be safely reduced to a deterministic comparison route to `human_review`.

`interest` routing is outside this policy gate. A not-interested reply should be skipped by the surrounding workflow rather than interpreted by the gate.

## Why

The next lookup is already known from `campaign_id`, so the Agent Tool protocol would add model selection, tool-call arguments, dispatch, and observation handling without adding useful decision-making.

Keeping Campaign rules minimal also avoids turning the gate into a general Campaign context object.

## Revisit when

Revisit this decision if real business requirements show that:

- deliverable or usage-right checks need structured upstream facts;
- multiple quotes can be mapped to explicit structured conditions;
- some Campaign rules are legitimately optional and need a distinct meaning from misconfiguration;
- the next business action genuinely becomes model-selected rather than workflow-known.
