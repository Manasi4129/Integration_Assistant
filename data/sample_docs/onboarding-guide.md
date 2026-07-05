# Seller Onboarding Guide

This guide walks a new seller through connecting their catalogue for the first time.

## Step 1: Create integration credentials

From the seller dashboard, open Settings > API Access and generate a client ID and
secret. Store the secret securely; it is shown only once. Credentials are scoped to a
single marketplace account.

## Step 2: Map your categories

Download the current category tree from the dashboard and map each of your internal
product categories to a marketplace leaf category. Only leaf categories are valid for
listings. Unmapped products will be rejected with CAT-020 at feed time.

## Step 3: Prepare your first feed

Export your catalogue to CSV or JSON following the Product Feed Specification. Start
with a small feed of 10–20 products to validate your mapping before uploading your full
catalogue. This makes early errors much easier to read and fix.

## Step 4: Submit and review

Upload the feed and wait for the validation report. Address any rejected rows using the
Feed Error Code Reference, then resubmit. Remember the limit of 4 feeds per hour when
iterating.

## Step 5: Go live

Once your test feed ingests cleanly, upload your full catalogue. Listings typically
appear in search within 30 minutes. Inventory and price updates can then be sent as
incremental feeds containing only changed rows.

## Common first-time issues

Most first-feed rejections come from category mapping (CAT-020) and image URLs that are
not HTTPS (IMG-030). Validating a small sample first avoids repeating the same error
across thousands of rows.
