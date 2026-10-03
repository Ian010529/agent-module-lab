from datetime import date

import pytest
from pydantic import ValidationError

from creator_reply.schemas import CreatorReply, Delivery, Quote


def test_exact_current_quote():
    reply = CreatorReply(
        interest="interested",
        quotes=[
            Quote(
                currency="GBP",
                conditions="one TikTok video",
                quote_basis="current_quote",
                amount_type="exact",
                amount=1200,
            )
        ],
    )
    assert reply.quotes is not None
    assert reply.quotes[0].amount == 1200


def test_usual_approximate_quote_can_have_missing_currency():
    quote = Quote(
        currency=None,
        conditions="TikTok; depends on usage rights",
        quote_basis="usual_rate",
        amount_type="approximate",
        amount=1500,
    )
    assert quote.currency is None
    assert quote.quote_basis == "usual_rate"


def test_range_quote_preserves_bounds():
    quote = Quote(
        currency="GBP",
        conditions="TikTok depending on usage",
        quote_basis="usual_rate",
        amount_type="range",
        min_amount=1000,
        max_amount=1500,
    )
    assert quote.amount is None
    assert (quote.min_amount, quote.max_amount) == (1000, 1500)


def test_multiple_conditional_quotes_keep_price_condition_relationship():
    reply = CreatorReply(
        interest="interested",
        quotes=[
            Quote(
                currency="GBP",
                conditions="one TikTok video",
                quote_basis="current_quote",
                amount_type="exact",
                amount=1200,
            ),
            Quote(
                currency="GBP",
                conditions="one TikTok video + 3 months paid usage",
                quote_basis="current_quote",
                amount_type="exact",
                amount=1600,
            ),
        ],
    )
    assert reply.quotes is not None
    assert len(reply.quotes) == 2
    assert "paid usage" in (reply.quotes[1].conditions or "")


def test_no_quote_is_none_not_extraction_failure():
    reply = CreatorReply(interest="not_interested", quotes=None, delivery=None)
    assert reply.quotes is None


def test_approximate_delivery_preserves_text_without_fake_date():
    delivery = Delivery(
        delivery_type="approximate",
        raw_text="sometime next month",
    )
    assert delivery.normalized_date is None
    assert delivery.start_date is None
    assert delivery.end_date is None


def test_deadline_uses_single_normalized_date():
    delivery = Delivery(
        delivery_type="deadline",
        normalized_date=date(2026, 10, 20),
        raw_text="by 20 October",
    )
    assert delivery.normalized_date == date(2026, 10, 20)


def test_invalid_exact_quote_with_range_fields_fails():
    with pytest.raises(ValidationError):
        Quote(
            currency="GBP",
            conditions="one TikTok video",
            quote_basis="current_quote",
            amount_type="exact",
            amount=1200,
            min_amount=1000,
            max_amount=1500,
        )


def test_invalid_range_missing_bound_fails():
    with pytest.raises(ValidationError):
        Quote(
            currency="GBP",
            conditions="TikTok",
            quote_basis="current_quote",
            amount_type="range",
            min_amount=1000,
        )


def test_currency_is_normalized_to_uppercase_code():
    quote = Quote(
        currency="gbp",
        conditions="one TikTok video",
        quote_basis="current_quote",
        amount_type="exact",
        amount=1200,
    )
    assert quote.currency == "GBP"


def test_currency_symbol_is_rejected_after_extraction():
    with pytest.raises(ValidationError):
        Quote(
            currency="£",
            conditions="one TikTok video",
            quote_basis="current_quote",
            amount_type="exact",
            amount=1200,
        )


def test_empty_quote_list_is_rejected_use_none_instead():
    with pytest.raises(ValidationError):
        CreatorReply(interest="not_interested", quotes=[])


def test_approximate_delivery_cannot_invent_normalized_date():
    with pytest.raises(ValidationError):
        Delivery(
            delivery_type="approximate",
            normalized_date=date(2026, 10, 15),
            raw_text="sometime next month",
        )
