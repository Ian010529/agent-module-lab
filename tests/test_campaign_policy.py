from datetime import date

import pytest

from campaign_policy.gate import evaluate_campaign_policy, evaluate_policy
from campaign_policy.lookup import CampaignRulesLookupError, lookup_campaign_rules
from campaign_policy.schemas import CampaignRules
from creator_reply.schemas import CreatorReply, Delivery, Quote


RULES = CampaignRules(
    campaign_id="cmp-001",
    max_budget=1500,
    currency="USD",
    latest_delivery_date=date(2026, 11, 30),
)


def current_quote(
    *,
    amount_type="exact",
    amount=None,
    min_amount=None,
    max_amount=None,
    currency="USD",
    conditions=None,
):
    return Quote(
        currency=currency,
        conditions=conditions,
        quote_basis="current_quote",
        amount_type=amount_type,
        amount=amount,
        min_amount=min_amount,
        max_amount=max_amount,
    )


def exact_delivery(day: date):
    return Delivery(
        delivery_type="exact_date",
        normalized_date=day,
        raw_text=day.isoformat(),
    )


def reply_with(*, quotes, delivery, interest="interested"):
    return CreatorReply(
        interest=interest,
        quotes=quotes,
        delivery=delivery,
    )


def test_lookup_returns_valid_campaign_rules_from_known_id():
    records = {
        "cmp-001": {
            "max_budget": 1500,
            "currency": "usd",
            "latest_delivery_date": date(2026, 11, 30),
        }
    }

    rules = lookup_campaign_rules("cmp-001", records.get)

    assert rules == RULES


def test_lookup_fails_when_campaign_does_not_exist():
    with pytest.raises(CampaignRulesLookupError, match="campaign_not_found"):
        lookup_campaign_rules("missing", {}.get)


def test_lookup_fails_when_campaign_rules_are_incomplete():
    records = {
        "cmp-001": {
            "max_budget": 1500,
            "latest_delivery_date": date(2026, 11, 30),
        }
    }

    with pytest.raises(CampaignRulesLookupError, match="invalid_campaign_rules"):
        lookup_campaign_rules("cmp-001", records.get)


def test_exact_current_quote_within_budget_and_delivery_deadline_is_within_policy():
    reply = reply_with(
        quotes=[current_quote(amount=1200)],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "within_policy"
    assert decision.reasons == []


def test_exact_current_quote_at_budget_limit_is_within_policy():
    reply = reply_with(
        quotes=[current_quote(amount=1500)],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    assert evaluate_policy(reply, RULES).status == "within_policy"


def test_exact_current_quote_over_budget_is_outside_policy():
    reply = reply_with(
        quotes=[current_quote(amount=1800)],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "outside_policy"
    assert "over_budget" in decision.reasons


def test_currency_mismatch_is_outside_policy():
    reply = reply_with(
        quotes=[current_quote(amount=1200, currency="EUR")],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "outside_policy"
    assert "currency_mismatch" in decision.reasons


def test_missing_creator_currency_is_missing_information():
    reply = reply_with(
        quotes=[current_quote(amount=1200, currency=None)],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "missing_information"
    assert "missing_quote_currency" in decision.reasons


def test_natural_language_quote_conditions_require_human_review():
    reply = reply_with(
        quotes=[current_quote(amount=1200, conditions="paid usage may cost extra")],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "human_review"
    assert "quote_conditions_require_review" in decision.reasons


def test_current_quote_range_fully_within_budget_is_allowed():
    reply = reply_with(
        quotes=[
            current_quote(
                amount_type="range",
                min_amount=1000,
                max_amount=1400,
            )
        ],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    assert evaluate_policy(reply, RULES).status == "within_policy"


def test_current_quote_range_fully_above_budget_is_outside_policy():
    reply = reply_with(
        quotes=[
            current_quote(
                amount_type="range",
                min_amount=1600,
                max_amount=1800,
            )
        ],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "outside_policy"
    assert "range_over_budget" in decision.reasons


def test_current_quote_range_crossing_budget_requires_human_review():
    reply = reply_with(
        quotes=[
            current_quote(
                amount_type="range",
                min_amount=1200,
                max_amount=1800,
            )
        ],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "human_review"
    assert "range_crosses_budget" in decision.reasons


def test_starting_from_quote_above_budget_is_outside_policy():
    reply = reply_with(
        quotes=[current_quote(amount_type="starting_from", amount=1600)],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    assert evaluate_policy(reply, RULES).status == "outside_policy"


def test_starting_from_quote_at_or_below_budget_requires_human_review():
    reply = reply_with(
        quotes=[current_quote(amount_type="starting_from", amount=1200)],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "human_review"
    assert "starting_from_total_unknown" in decision.reasons


def test_approximate_quote_above_budget_is_outside_policy():
    reply = reply_with(
        quotes=[current_quote(amount_type="approximate", amount=1600)],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    assert evaluate_policy(reply, RULES).status == "outside_policy"


def test_approximate_quote_at_or_below_budget_requires_human_review():
    reply = reply_with(
        quotes=[current_quote(amount_type="approximate", amount=1200)],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "human_review"
    assert "approximate_quote_requires_review" in decision.reasons


def test_usual_rate_means_current_quote_is_missing():
    quote = Quote(
        currency="USD",
        conditions=None,
        quote_basis="usual_rate",
        amount_type="exact",
        amount=1200,
    )
    reply = reply_with(
        quotes=[quote],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "missing_information"
    assert "missing_current_quote" in decision.reasons


def test_unclear_quote_basis_requires_human_review():
    quote = Quote(
        currency="USD",
        conditions=None,
        quote_basis="unclear",
        amount_type="exact",
        amount=1200,
    )
    reply = reply_with(
        quotes=[quote],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "human_review"
    assert "unclear_quote_basis" in decision.reasons


def test_no_quote_is_missing_information():
    reply = reply_with(
        quotes=None,
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "missing_information"
    assert "missing_quote" in decision.reasons


def test_multiple_quotes_require_human_review_without_auto_selecting_one():
    reply = reply_with(
        quotes=[
            current_quote(amount=1200),
            current_quote(amount=1400),
        ],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "human_review"
    assert "multiple_quotes_require_review" in decision.reasons


def test_missing_delivery_is_missing_information():
    reply = reply_with(
        quotes=[current_quote(amount=1200)],
        delivery=None,
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "missing_information"
    assert "missing_delivery" in decision.reasons


def test_delivery_deadline_equal_to_campaign_deadline_is_within_policy():
    delivery = Delivery(
        delivery_type="deadline",
        normalized_date=date(2026, 11, 30),
        raw_text="by 30 November",
    )
    reply = reply_with(
        quotes=[current_quote(amount=1200)],
        delivery=delivery,
    )

    assert evaluate_policy(reply, RULES).status == "within_policy"


def test_delivery_after_deadline_is_outside_policy():
    reply = reply_with(
        quotes=[current_quote(amount=1200)],
        delivery=exact_delivery(date(2026, 12, 5)),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "outside_policy"
    assert "delivery_after_deadline" in decision.reasons


def test_delivery_range_fully_within_deadline_is_allowed():
    delivery = Delivery(
        delivery_type="date_range",
        start_date=date(2026, 11, 10),
        end_date=date(2026, 11, 25),
        raw_text="10-25 November",
    )
    reply = reply_with(quotes=[current_quote(amount=1200)], delivery=delivery)

    assert evaluate_policy(reply, RULES).status == "within_policy"


def test_delivery_range_fully_after_deadline_is_outside_policy():
    delivery = Delivery(
        delivery_type="date_range",
        start_date=date(2026, 12, 1),
        end_date=date(2026, 12, 10),
        raw_text="1-10 December",
    )
    reply = reply_with(quotes=[current_quote(amount=1200)], delivery=delivery)

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "outside_policy"
    assert "delivery_range_after_deadline" in decision.reasons


def test_delivery_range_crossing_deadline_requires_human_review():
    delivery = Delivery(
        delivery_type="date_range",
        start_date=date(2026, 11, 25),
        end_date=date(2026, 12, 5),
        raw_text="25 November to 5 December",
    )
    reply = reply_with(quotes=[current_quote(amount=1200)], delivery=delivery)

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "human_review"
    assert "delivery_range_crosses_deadline" in decision.reasons


def test_approximate_delivery_requires_human_review():
    delivery = Delivery(
        delivery_type="approximate",
        raw_text="late November",
    )
    reply = reply_with(quotes=[current_quote(amount=1200)], delivery=delivery)

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "human_review"
    assert "approximate_delivery_requires_review" in decision.reasons


def test_status_priority_is_outside_then_human_then_missing_then_within():
    reply = reply_with(
        quotes=[current_quote(amount=1800, currency=None)],
        delivery=Delivery(
            delivery_type="approximate",
            raw_text="late November",
        ),
    )

    decision = evaluate_policy(reply, RULES)

    assert decision.status == "outside_policy"
    assert "over_budget" in decision.reasons
    assert "missing_quote_currency" in decision.reasons
    assert "approximate_delivery_requires_review" in decision.reasons


def test_policy_gate_does_not_route_on_interest():
    reply = reply_with(
        interest="not_interested",
        quotes=[current_quote(amount=1200)],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    assert evaluate_policy(reply, RULES).status == "within_policy"


def test_evaluate_campaign_policy_connects_direct_lookup_to_gate():
    records = {
        "cmp-001": {
            "max_budget": 1500,
            "currency": "USD",
            "latest_delivery_date": date(2026, 11, 30),
        }
    }
    reply = reply_with(
        quotes=[current_quote(amount=1200)],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    decision = evaluate_campaign_policy(reply, "cmp-001", records.get)

    assert decision.status == "within_policy"


def test_evaluate_campaign_policy_stops_on_lookup_failure():
    reply = reply_with(
        quotes=[current_quote(amount=1200)],
        delivery=exact_delivery(date(2026, 11, 20)),
    )

    with pytest.raises(CampaignRulesLookupError, match="campaign_not_found"):
        evaluate_campaign_policy(reply, "missing", {}.get)
