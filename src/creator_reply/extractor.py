from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel

from .schemas import CreatorReply

SYSTEM_PROMPT = """You extract business facts from a creator reply.
Return only facts supported by the reply.
Do not infer missing currency, dates, prices, or commercial commitments.
When currency is explicit, return a three-letter currency code such as GBP or USD.
Preserve uncertainty: distinguish current quotes from usual rates and exact amounts from approximate, range, or starting-from prices.
If the reply provides no quote, set quotes to null.
For approximate delivery wording that cannot be safely normalized to an exact date or date range, preserve it in raw_text and leave normalized date fields null.
"""


class StructuredReplyModel(Protocol):
    def invoke(self, messages: list[dict[str, str]]) -> Any: ...


class StructuredOutputCapableModel(Protocol):
    def with_structured_output(self, schema: type[BaseModel]) -> StructuredReplyModel: ...


def extract_creator_reply(
    model: StructuredOutputCapableModel,
    reply_text: str,
) -> CreatorReply:
    """Extract source-backed creator-reply facts using structured output.

    The caller chooses the concrete model/provider. This slice only depends on the
    narrow structured-output capability used by the reference implementation.
    """
    structured_model = model.with_structured_output(CreatorReply)
    result = structured_model.invoke(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": reply_text},
        ]
    )
    return CreatorReply.model_validate(result)
