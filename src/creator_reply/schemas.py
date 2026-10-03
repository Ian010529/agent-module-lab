from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Interest = Literal["interested", "not_interested", "conditional", "unclear"]
QuoteBasis = Literal["current_quote", "usual_rate", "unclear"]
AmountType = Literal["exact", "approximate", "range", "starting_from"]
DeliveryType = Literal["exact_date", "deadline", "date_range", "approximate"]


class Quote(BaseModel):
    """A creator-provided price statement and the conditions attached to it."""

    model_config = ConfigDict(extra="forbid")

    currency: str | None = Field(
        default=None,
        description="Explicit currency code or symbol-derived currency. None when not stated.",
    )
    conditions: str | None = Field(
        default=None,
        description="What this price applies to, such as deliverable or usage-right conditions.",
    )
    quote_basis: QuoteBasis = Field(
        description="Whether this is a current quote, a usual rate, or unclear from the reply."
    )
    amount_type: AmountType = Field(
        description="How precisely the amount is expressed in the reply."
    )
    amount: float | None = None
    min_amount: float | None = None
    max_amount: float | None = None

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().upper()
        if len(normalized) != 3 or not normalized.isalpha():
            raise ValueError("currency must be a three-letter code such as GBP or USD")
        return normalized

    @model_validator(mode="after")
    def validate_amount_shape(self) -> "Quote":
        if self.amount_type == "range":
            if self.amount is not None:
                raise ValueError("range quotes must not set amount")
            if self.min_amount is None or self.max_amount is None:
                raise ValueError("range quotes require min_amount and max_amount")
            if self.min_amount > self.max_amount:
                raise ValueError("min_amount cannot exceed max_amount")
            return self

        if self.amount is None:
            raise ValueError(f"{self.amount_type} quotes require amount")
        if self.min_amount is not None or self.max_amount is not None:
            raise ValueError(
                f"{self.amount_type} quotes must not set min_amount or max_amount"
            )
        return self


class Delivery(BaseModel):
    """Delivery timing explicitly expressed in the creator reply."""

    model_config = ConfigDict(extra="forbid")

    delivery_type: DeliveryType
    normalized_date: date | None = None
    start_date: date | None = None
    end_date: date | None = None
    raw_text: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_date_shape(self) -> "Delivery":
        if self.delivery_type in {"exact_date", "deadline"}:
            if self.normalized_date is None:
                raise ValueError(f"{self.delivery_type} requires date")
            if self.start_date is not None or self.end_date is not None:
                raise ValueError(
                    f"{self.delivery_type} must not set start_date or end_date"
                )
            return self

        if self.delivery_type == "date_range":
            if self.normalized_date is not None:
                raise ValueError("date_range must not set date")
            if self.start_date is None or self.end_date is None:
                raise ValueError("date_range requires start_date and end_date")
            if self.start_date > self.end_date:
                raise ValueError("start_date cannot exceed end_date")
            return self

        if (
            self.normalized_date is not None
            or self.start_date is not None
            or self.end_date is not None
        ):
            raise ValueError("approximate delivery must not invent normalized dates")
        return self


class CreatorReply(BaseModel):
    """Facts extracted from a creator reply for downstream workflow decisions."""

    model_config = ConfigDict(extra="forbid")

    interest: Interest
    quotes: list[Quote] | None = None
    delivery: Delivery | None = None

    @model_validator(mode="after")
    def reject_empty_quote_list(self) -> "CreatorReply":
        if self.quotes == []:
            raise ValueError("use quotes=None when the reply contains no quote information")
        return self
