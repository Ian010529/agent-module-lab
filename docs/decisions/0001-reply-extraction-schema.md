# Reply Extraction schema boundary

## Decision

The first Creator Reply extraction slice returns only source-backed business facts needed by downstream workflow decisions:

- `interest`
- `quotes`
- `delivery`

A `Quote` separates three independent dimensions:

- `quote_basis`: whether the number is a current quote, a usual rate, or unclear;
- `amount_type`: exact, approximate, range, or starting-from;
- `conditions`: what the price applies to.

`quotes=None` means the reply contains no quote information. An empty quote list is rejected so it cannot silently acquire a second meaning.

Currency is normalized to a three-letter code when explicitly present and remains `None` when absent. Delivery keeps `raw_text`; exact/deadline/range dates use normalized date fields, while approximate wording must not invent a date.

## Why

A single amount field loses relationships between price, pricing conditions, and uncertainty. The chosen structure preserves those semantics while keeping derived business decisions such as over-budget checks outside the LLM extraction layer.

## Revisit when

Revisit this schema if real creator replies require additional quote bases, recurring/complex delivery windows, or structured deliverable fields that downstream decisions cannot reliably obtain from `conditions`.
