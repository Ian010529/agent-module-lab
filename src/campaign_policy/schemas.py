from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


PolicyStatus = Literal[
    "within_policy",
    "outside_policy",
    "missing_information",
    "human_review",
]


class CampaignRules(BaseModel):
    """Validated campaign rules required by the Slice 2 policy gate."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str
    max_budget: float
    currency: str
    latest_delivery_date: date

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        normalized = value.strip().upper()
        if len(normalized) != 3 or not normalized.isalpha():
            raise ValueError("currency must be a three-letter code such as GBP or USD")
        return normalized


class PolicyDecision(BaseModel):
    """Deterministic result of comparing CreatorReply facts with CampaignRules."""

    model_config = ConfigDict(extra="forbid")

    status: PolicyStatus
    reasons: list[str] = Field(default_factory=list)
