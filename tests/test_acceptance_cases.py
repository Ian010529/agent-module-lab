import json
from pathlib import Path

from creator_reply.schemas import CreatorReply


def test_acceptance_case_expected_outputs_match_schema():
    cases = json.loads(
        (Path(__file__).with_name("reply_extraction_cases.json")).read_text()
    )

    assert len(cases) == 7
    for case in cases:
        CreatorReply.model_validate(case["expected"])
