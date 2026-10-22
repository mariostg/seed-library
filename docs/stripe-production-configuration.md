# Stripe Production Configuration

This guide switches the donation integration from Stripe test mode to live mode on the Debian VPS.

## Before You Start

The production application uses:

- Django/Gunicorn for the web process
- A manually managed Celery worker
- Stripe Dashboard webhooks
- SMTP for email delivery

The VPS does not rely on the project Dockerfile or Procfile.

Never place real Stripe credentials in Git, chat messages, screenshots, or logs.

## Stripe Live Webhook Endpoint

In the Stripe Dashboard:

1. Switch to **Live mode**.
2. Go to **Developers -> Webhooks**.
3. Create or select this endpoint:

   ```text
   https://owsl.mariostg.com/stripe/webhook/
   ```

4. Subscribe the endpoint to:
   - `checkout.session.completed`
   - `invoice.paid`
   - `invoice.payment_failed`

5. Open the endpoint actions menu and choose **Roll signing secret**.
6. Copy the new `whsec_...` value.

Test-mode and live-mode webhook endpoints have different signing secrets. The local
`stripe listen` secret is only for local CLI forwarding and must not be used in production.

## Rotate Stripe API Keys

Rotate both the live and test secret keys if either has been exposed:

1. In Stripe Dashboard, select the appropriate mode.
2. Go to **Developers -> API keys**.
3. Choose **Roll key** for the secret key.
4. Copy the replacement key.
5. Update the VPS `.env` immediately.
6. After confirming the application works, revoke the old key.

Publishable keys (`pk_...`) are not secret. They do not normally need rotation, but the
production application must use a live publishable key.

## VPS Environment Variables

For production, set the live Stripe keys and disable test-key selection:

```dotenv
TEST_STRIPE=False
STRIPE_PUBLISHABLE_KEY=pk_live_replace_me
STRIPE_SECRET_KEY=sk_live_replace_me
STRIPE_WEBHOOK_SECRET=whsec_replace_me
STRIPE_DONATION_CURRENCY=cad
STRIPE_DONATION_MIN_AMOUNT=1.00
```

Remove or comment out test-only values unless they are intentionally retained for a
separate test deployment:

```dotenv
# STRIPE_SECRET_KEY_TEST=sk_test_replace_me
# STRIPE_PUBLISHABLE_KEY_TEST=pk_test_replace_me
```

The setting `TEST_STRIPE=True` makes Django use `STRIPE_SECRET_KEY_TEST` and
`STRIPE_PUBLISHABLE_KEY_TEST`, even when live keys are also present. Production must
set it to `False` or remove it.

## Email Settings

Confirm that production SMTP credentials and a permitted sender address are configured:

```dotenv
EMAIL_MODE=live
SMTP_EMAIL_HOST=replace_with_smtp_host
SMTP_EMAIL_HOST_USER=replace_with_smtp_user
SMTP_EMAIL_HOST_PASSWORD=replace_with_smtp_password
SMTP_EMAIL_PORT=587
SMTP_EMAIL_USE_TLS=True
SMTP_EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=replace_with_authorized_sender
```

`EMAIL_MODE=live` selects the live SMTP defaults in this project; it does not by itself
create an email-provider account or validate the sender address.

Use either STARTTLS on port 587 or implicit SSL on port 465, never both:

```dotenv
# STARTTLS
SMTP_EMAIL_PORT=587
SMTP_EMAIL_USE_TLS=True
SMTP_EMAIL_USE_SSL=False
```

```dotenv
# Implicit SSL
SMTP_EMAIL_PORT=465
SMTP_EMAIL_USE_TLS=False
SMTP_EMAIL_USE_SSL=True
```

## Restart Services

After changing `.env`, restart every process that loads Django settings.

Restart Gunicorn:

```bash
sudo systemctl restart djbp.service
sudo systemctl status djbp.service
```

Stop and restart the manually managed Celery worker:

```bash
celery -A main.celery worker --loglevel=info
```

Keep the worker running in a service manager such as systemd, `screen`, or `tmux` so it
survives logout. The worker must use the same project directory, virtual environment,
and `.env` as Django.

## Production Verification

1. In Stripe Live mode, confirm the webhook endpoint is enabled.
2. Make a small real donation using a real payment method. Test card `4242 4242 4242 4242` works only in Test mode.
3. In Stripe Dashboard, open the endpoint's **Recent deliveries**.
4. Confirm `checkout.session.completed` returns HTTP `200`.
5. In Django admin, check `/admin/project/stripewebhookevent/`.
6. Confirm a `Donation` record has status `succeeded`.
7. Confirm the Celery worker logs show `send_donation_receipt_task`.
8. Confirm the thank-you email was delivered.

Expected behavior:

- HTTP `200`: the webhook was accepted and processed.
- HTTP `400`: the webhook signing secret is wrong, or the endpoint is using the wrong
  Stripe mode.
- HTTP `500`: Django received the webhook but failed while processing it; inspect the
  `processing_error` field on `StripeWebhookEvent` and the Gunicorn logs.
- No delivery attempt: Stripe is not configured to send that event to this endpoint, or
  the wrong Stripe account/mode is being viewed.

## Troubleshooting Commands

Check the web service:

```bash
sudo journalctl -u djbp.service -f
```

Check the Celery worker if it has a systemd service:

```bash
sudo journalctl -u djbp-celery-worker.service -f
```

If Celery is running manually, inspect the terminal or session where it was started.

Check nginx while sending a webhook or making a donation:

```bash
sudo tail -f /var/log/nginx/access.log /var/log/nginx/error.log
```

A plain unsigned request is useful only for checking routing:

```bash
curl -i -X POST https://owsl.mariostg.com/stripe/webhook/ \
  -H "Content-Type: application/json" \
  -d '{"type":"test"}'
```

A response of HTTP `400` is expected because the request has no valid Stripe signature.
It confirms that nginx and Django route the webhook URL correctly; it will not create a
`StripeWebhookEvent` row.
