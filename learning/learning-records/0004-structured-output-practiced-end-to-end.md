# Structured output is now practiced in the project

The user completed the Creator Reply structured-extraction slice through real-model verification, not just schema-only or fake-model tests. Future sessions can assume they have practiced the full path from source text to structured output to schema validation and can move on without re-teaching the basic boundary between semantic extraction and deterministic validation.

## Evidence

The project implementation uses `with_structured_output(CreatorReply)`, deterministic schema validators, retained acceptance cases, and the real-model verification passed.
