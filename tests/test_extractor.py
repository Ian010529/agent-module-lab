from creator_reply.extractor import extract_creator_reply
from creator_reply.schemas import CreatorReply


class FakeStructuredModel:
    def __init__(self, result):
        self.result = result
        self.messages = None

    def invoke(self, messages):
        self.messages = messages
        return self.result


class FakeBaseModel:
    def __init__(self, result):
        self.structured = FakeStructuredModel(result)
        self.schema = None

    def with_structured_output(self, schema):
        self.schema = schema
        return self.structured


def test_extractor_wraps_model_with_creator_reply_schema_and_uses_no_guess_prompt():
    model = FakeBaseModel(
        {
            "interest": "interested",
            "quotes": [
                {
                    "currency": None,
                    "conditions": "TikTok",
                    "quote_basis": "usual_rate",
                    "amount_type": "approximate",
                    "amount": 1500,
                    "min_amount": None,
                    "max_amount": None,
                }
            ],
            "delivery": None,
        }
    )

    result = extract_creator_reply(model, "I usually charge around 1500 for TikTok.")

    assert model.schema is CreatorReply
    assert result.quotes is not None
    assert result.quotes[0].currency is None
    assert "Do not infer missing currency" in model.structured.messages[0]["content"]
