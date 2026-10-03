from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from creator_reply.schemas import CreatorReply, Delivery, Quote

from .lookup import lookup_campaign_rules
from .schemas import CampaignRules, PolicyDecision


_STATUS_PRIORITY = {
    "within_policy": 0,
    "missing_information": 1,
    "human_review": 2,
    "outside_policy": 3,
}


def _final_status(statuses: list[str]) -> str:
    if not statuses:
        return "within_policy"
    return max(statuses, key=_STATUS_PRIORITY.__getitem__)


def _add(
    statuses: list[str],
    reasons: list[str],
    status: str,
    reason: str,
) -> None:
    statuses.append(status)
    reasons.append(reason)


def _evaluate_quote(
    quote: Quote,
    rules: CampaignRules,
    statuses: list[str],
    reasons: list[str],
) -> None:
    if quote.quote_basis == "usual_rate":
        _add(statuses, reasons, "missing_information", "missing_current_quote")
        return

    if quote.quote_basis == "unclear":
        _add(statuses, reasons, "human_review", "unclear_quote_basis")
        return

    if quote.conditions is not None:
        _add(
            statuses,
            reasons,
            "human_review",
            "quote_conditions_require_review",
        )

    if quote.currency is None:
        _add(statuses, reasons, "missing_information", "missing_quote_currency")
    elif quote.currency != rules.currency:
        _add(statuses, reasons, "outside_policy", "currency_mismatch")

    if quote.amount_type == "exact":
        if quote.amount > rules.max_budget:
            _add(statuses, reasons, "outside_policy", "over_budget")
        return

    if quote.amount_type == "range":
        if quote.min_amount > rules.max_budget:
            _add(statuses, reasons, "outside_policy", "range_over_budget")
        elif quote.max_amount > rules.max_budget:
            _add(statuses, reasons, "human_review", "range_crosses_budget")
        return

    if quote.amount_type == "starting_from":
        if quote.amount > rules.max_budget:
            _add(statuses, reasons, "outside_policy", "over_budget")
        else:
            _add(
                statuses,
                reasons,
                "human_review",
                "starting_from_total_unknown",
            )
        return

    if quote.amount_type == "approximate":
        if quote.amount > rules.max_budget:
            _add(statuses, reasons, "outside_policy", "over_budget")
        else:
            _add(
                statuses,
                reasons,
                "human_review",
                "approximate_quote_requires_review",
            )


def _evaluate_delivery(
    delivery: Delivery | None,
    rules: CampaignRules,
    statuses: list[str],
    reasons: list[str],
) -> None:
    if delivery is None:
        _add(statuses, reasons, "missing_information", "missing_delivery")
        return

    if delivery.delivery_type in {"exact_date", "deadline"}:
        if delivery.normalized_date > rules.latest_delivery_date:
            _add(
                statuses,
                reasons,
                "outside_policy",
                "delivery_after_deadline",
            )
        return

    if delivery.delivery_type == "date_range":
        if delivery.start_date > rules.latest_delivery_date:
            _add(
                statuses,
                reasons,
                "outside_policy",
                "delivery_range_after_deadline",
            )
        elif delivery.end_date > rules.latest_delivery_date:
            _add(
                statuses,
                reasons,
                "human_review",
                "delivery_range_crosses_deadline",
            )
        return

    if delivery.delivery_type == "approximate":
        _add(
            statuses,
            reasons,
            "human_review",
            "approximate_delivery_requires_review",
        )


def evaluate_policy(
    reply: CreatorReply,
    rules: CampaignRules,
) -> PolicyDecision:
    """Evaluate only deterministic Slice 2 policy rules.

    Interest routing is deliberately outside this gate. Semantic quote conditions
    and ambiguous/ranged facts are surfaced for human review rather than guessed.
    """

    statuses: list[str] = []
    reasons: list[str] = []

    if reply.quotes is None:
        _add(statuses, reasons, "missing_information", "missing_quote")
    elif len(reply.quotes) > 1:
        _add(
            statuses,
            reasons,
            "human_review",
            "multiple_quotes_require_review",
        )
    else:
        _evaluate_quote(reply.quotes[0], rules, statuses, reasons)

    _evaluate_delivery(reply.delivery, rules, statuses, reasons)

    return PolicyDecision(
        status=_final_status(statuses),
        reasons=reasons,
    )


def evaluate_campaign_policy(
    reply: CreatorReply,
    campaign_id: str,
    fetcher: Callable[[str], Mapping[str, Any] | CampaignRules | None],
) -> PolicyDecision:
    """Directly load rules for the known campaign and run the deterministic gate."""

    rules = lookup_campaign_rules(campaign_id, fetcher)
    return evaluate_policy(reply, rules)
