from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from pydantic import ValidationError

from .schemas import CampaignRules


class CampaignRulesLookupError(RuntimeError):
    """Campaign rules could not be loaded as a valid gate input."""


def lookup_campaign_rules(
    campaign_id: str,
    fetcher: Callable[[str], Mapping[str, Any] | CampaignRules | None],
) -> CampaignRules:
    """Directly fetch and validate the rules for a known campaign id.

    The fetcher is intentionally thin so a later real API/DB adapter can replace
    the in-memory test source without turning this known next step into an Agent Tool.
    """

    raw = fetcher(campaign_id)
    if raw is None:
        raise CampaignRulesLookupError("campaign_not_found")

    if isinstance(raw, CampaignRules):
        if raw.campaign_id != campaign_id:
            raise CampaignRulesLookupError("campaign_id_mismatch")
        return raw

    payload = dict(raw)
    payload["campaign_id"] = campaign_id

    try:
        return CampaignRules.model_validate(payload)
    except (ValidationError, TypeError, ValueError) as exc:
        raise CampaignRulesLookupError("invalid_campaign_rules") from exc
