# Product Feed Specification (v3)

This document describes the required and optional fields for uploading a product
catalogue feed. Feeds may be submitted as CSV or JSON. All feeds are validated against
this specification before ingestion.

## Required fields

- `sku` — Unique seller SKU. Must be 3–40 characters, alphanumeric plus hyphens. Must be
  unique within the feed; duplicate SKUs cause the whole row to be rejected.
- `title` — Product title, 5–200 characters. Titles over 200 characters are truncated
  with a warning, not rejected.
- `price` — Decimal with exactly two places, in the account's default currency. A price
  of 0 or below is rejected.
- `quantity` — Non-negative integer. A quantity of 0 marks the listing as out of stock
  but does not reject it.
- `category_id` — Must match a value from the marketplace category tree. Unknown
  category IDs are rejected.

## Optional fields

- `brand` — Recommended. Missing brand triggers a warning and may reduce search ranking.
- `gtin` — Global Trade Item Number. If present it must pass checksum validation.
- `images` — Pipe-separated list of HTTPS URLs. HTTP (non-secure) URLs are rejected.

## Validation order

Feeds are validated field by field, top to bottom. The first hard error on a row
rejects that row; remaining rows are still processed. A feed with any rejected rows
still completes, and a validation report is generated listing every rejected row and
the reason.

## Rate limits

A single account may submit at most 4 feeds per hour. Feeds submitted beyond this limit
receive error FEED-429 and are not queued.
