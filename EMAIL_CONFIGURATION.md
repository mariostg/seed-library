<!--
Email configuration and testing guide for the project.

This file documents the current implementation: emails are sent by Celery tasks
that are enqueued from `create_order_from_cart()` using `transaction.on_commit()`.
-->

# Email Configuration Guide

This guide explains how to configure email sending for order confirmations and donation thank you emails.

## Overview

The application sends two kinds of transactional emails related to orders:

- Order confirmation (when an order is placed)
- Donation thank-you (only if a donation amount > 0)

Notes about implementation (current codebase):

- Email sending is performed asynchronously by Celery tasks defined in `project/tasks.py`.
- Orders and their `OrderItem`s are created inside a database transaction; Celery tasks are enqueued using `transaction.on_commit(...)` to ensure tasks are scheduled only after the DB commit.

## Configuration

### 1. Required Settings in `main/settings.py`

Add or verify the following email-related settings (examples):

```python
# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")  # e.g., 'smtp.gmail.com'

EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "true").lower() in {
    "1",
    "true",
    "yes",
    "on",
}
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "false").lower() in {
    "1",
    "true",
    "yes",
    "on",
}
# Note: EMAIL_USE_TLS and EMAIL_USE_SSL must not both be True.
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
DEFAULT_BCC_EMAIL = os.environ.get("DEFAULT_BCC_EMAIL")

# Celery broker (Redis example)
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
)
```

### 2. Environment Variables (Recommended)

Store credentials in environment variables or a `.env` file (project uses python-dotenv):

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_USE_SSL=false

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@example.com

DEFAULT_BCC_EMAIL=ops@example.com
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

Common SMTP combinations:

- STARTTLS (most providers): `EMAIL_PORT=587`, `EMAIL_USE_TLS=true`, `EMAIL_USE_SSL=false`
- Implicit SSL: `EMAIL_PORT=465`, `EMAIL_USE_TLS=false`, `EMAIL_USE_SSL=true`

## How It Works (current implementation)

- The checkout code calls `create_order_from_cart()` in `project/utils.py`.
- `create_order_from_cart()` wraps creation of the `Order` and its `OrderItem` rows inside a `transaction.atomic()` block.

- After creating the order and items, it schedules Celery tasks using `transaction.on_commit(...)`:
  - `send_order_confirmation_task.delay(order.id)` — enqueues order confirmation email
  - `send_donation_thank_you_task.delay(order.id)` — enqueues donation email (only if donation_amount > 0)

- The Celery tasks are defined in `project/tasks.py` and send emails by calling the helpers in `project/utils.py`.

This approach avoids the race condition of sending emails from Django `post_save` signals before related `OrderItem`s exist.

## Email Templates

Located in `project/templates/project/emails/`:

- `order_confirmation.html` (HTML)
- `order_confirmation.txt` (plain text)
- `donation_thank_you.html` (HTML)
- `donation_thank_you.txt` (plain text)

## Testing

### Quick SMTP test

```bash
python manage.py shell
```

Then in the shell:

```python
from django.core.mail import send_mail

send_mail(
    "Test", "Test body", "from@example.com", ["to@example.com"], fail_silently=False
)
```

### Test order email path (without Celery worker)

You can call the helper directly to verify template rendering:

```python
from project.models import Order
from project.utils import send_order_confirmation_email

order = Order.objects.first()
send_order_confirmation_email(order)
```

### Test enqueueing with Celery

1. Ensure Redis is running and a Celery worker is started (see Async Email Sending below).
2. Place an order via the app or call `create_order_from_cart()` in a Django shell — the Celery tasks should be enqueued after commit and the worker will process them.

## Async Email Sending (Celery)

The project now uses Celery to send emails asynchronously. Minimal steps to run locally:

1. Install packages:

```bash
pip install celery redis
```

2. Start Redis (macOS example):

```bash
# Homebrew
brew install redis
brew services start redis
# or run in foreground
redis-server
```

3. Start a Celery worker from the project root (venv active):

```bash
celery -A main.celery worker --loglevel=info
```

4. Verify tasks are processed in the worker logs when orders are placed.

If you prefer not to run a worker, you can still test email rendering by calling the sending helpers directly (see Testing above).

## Troubleshooting

- Redis connection refused: ensure Redis is running and `CELERY_BROKER_URL` points to the correct host/port. Try `redis-cli ping` — expect `PONG`.
- Celery cannot import tasks: ensure `main/celery.py` exists and `main.__init__.py` exposes the app (`from .celery import app as celery_app`).

- `STARTTLS extension not supported` or `server did not reply to HELO greeting`:
  - Verify SMTP host/port/encryption mode match provider docs.
  - Check outbound SMTP ports are open from your deployed host (587/465 may be blocked by provider/firewall).
  - If local works but production fails, suspect network/provider restrictions in production before credentials.

- Emails not sent: check Django logs, Celery worker logs, and SMTP provider errors. Use console backend for local inspection.

## Security Best Practices

1. **Never commit credentials** — Use environment variables.
2. **Use app-specific passwords** — Don't use your main account password.
3. **Enable TLS/SSL** — Always encrypt email transmission.
4. **Use a worker queue for reliability** — Celery + Redis provides retries and persistence.
5. **Monitor email logs** — Track sent/failed emails and worker health.

## Support

For issues or questions:

- Check Django email docs: https://docs.djangoproject.com/en/stable/topics/email/
- Check Celery docs: https://docs.celeryproject.org/
- Verify your SMTP provider's settings and credentials
- Inspect application and worker logs for errors
