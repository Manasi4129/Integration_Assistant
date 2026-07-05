# Feed Error Code Reference

Every rejected row in a validation report includes one of the following error codes.

## Row-level errors

- `SKU-001` — Duplicate SKU within the feed. Resolution: ensure each SKU appears only
  once per feed.
- `SKU-002` — SKU contains invalid characters. Only letters, digits, and hyphens are
  allowed. Resolution: strip spaces, underscores, and symbols.
- `PRICE-010` — Price is missing, zero, negative, or not formatted to two decimal
  places. Resolution: supply a positive decimal such as 19.99.
- `CAT-020` — Unknown category_id. The value does not exist in the current category
  tree. Resolution: re-map to a valid leaf category; parent categories are not
  accepted for listings.
- `IMG-030` — One or more image URLs are not HTTPS. Resolution: host images on an HTTPS
  endpoint and resubmit.
- `GTIN-040` — GTIN failed checksum validation. Resolution: verify the digits; a common
  cause is a transposed pair of numbers.

## Feed-level errors

- `FEED-429` — Rate limit exceeded (more than 4 feeds submitted in one hour). The feed
  is not queued. Resolution: wait until the rolling hour window clears and resubmit.
- `FEED-500` — Internal processing error. The feed was accepted but failed during
  ingestion. Resolution: resubmit once; if it recurs, raise a support ticket with the
  feed ID.

## Reading a validation report

A validation report lists, per rejected row, the SKU, the error code, and a
human-readable message. Rows that are not listed were ingested successfully. Warnings
(such as a missing brand) appear in a separate section and never block ingestion.
