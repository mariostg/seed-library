# Making a Donation

The catalogue now includes a dedicated donation page with Stripe checkout.

## Where to find it

- A Donate link is shown in the top navigation across catalogue pages.
- Main route: `/donate/`

## Donation options

- Preset amount buttons are available for quick selection.
- A custom amount field accepts decimal values.
- Donors can choose one-time or monthly recurring donation.

## Stripe checkout flow

- Submit donation form on `/donate/`
- Server creates Stripe Checkout session at `/donate/checkout/`
- Redirect to Stripe-hosted checkout
- Return URLs:
	- Success: `/donate/success/`
	- Cancel: `/donate/cancel/`

## Required environment variables

- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_SECRET_KEY`

Optional settings:

- `STRIPE_DONATION_CURRENCY` (default: `cad`)
- `STRIPE_DONATION_MIN_AMOUNT` (default: `1.00`)

## Webhook persistence

Donation success is persisted from Stripe webhook events, not from browser redirects.

- Webhook endpoint: `/stripe/webhook/`
- Required variable: `STRIPE_WEBHOOK_SECRET`

Persisted event types:

- `checkout.session.completed`
- `invoice.paid`
- `invoice.payment_failed`

Persistence tables:

- `StripeWebhookEvent`: stores received event IDs + payload for idempotency/audit.
- `Donation`: stores one-time and recurring donation payment records with Stripe IDs.

Idempotency:

- Stripe event IDs are unique in `StripeWebhookEvent`.
- Retries for the same event are accepted and ignored safely.
