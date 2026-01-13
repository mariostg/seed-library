# Email Configuration Guide

This guide explains how to configure email sending for order confirmations and donation thank you emails.

## Overview

The application automatically sends emails when:

1. A new order is created (order confirmation)
2. A donation is included with an order (donation thank you email)

## Configuration

### 1. Required Settings in `main/settings.py`

Add or modify the following email configuration settings:

```python
# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "your-email-provider.com"  # e.g., 'smtp.gmail.com', 'smtp.sendgrid.net'
EMAIL_PORT = 587  # Use 587 for TLS, 465 for SSL
EMAIL_USE_TLS = True  # Set to False if using SSL
EMAIL_USE_SSL = False  # Set to True if using SSL on port 465
EMAIL_HOST_USER = "your-email@example.com"
EMAIL_HOST_PASSWORD = "your-app-password-or-api-key"
DEFAULT_FROM_EMAIL = "noreply@example.com"  # The "From" address in emails
```

### 2. Email Provider Examples

#### Gmail

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-app-specific-password"  # NOT your regular password
DEFAULT_FROM_EMAIL = "noreply@example.com"
```

**Note:** For Gmail, you need to:

1. Enable 2-factor authentication
2. Generate an "App Password" at https://myaccount.google.com/apppasswords
3. Use the App Password (not your regular password)

#### SendGrid

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = "your-sendgrid-api-key"
DEFAULT_FROM_EMAIL = "noreply@example.com"
```

#### AWS SES

```python
EMAIL_BACKEND = "django_ses.SESBackend"  # Requires django-ses package
AWS_SES_REGION_NAME = "us-east-1"
AWS_SES_REGION_ENDPOINT = "email.us-east-1.amazonaws.com"
AWS_ACCESS_KEY_ID = "your-aws-access-key"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-key"
DEFAULT_FROM_EMAIL = "noreply@example.com"
```

#### Console Backend (Development Only)

For testing without actually sending emails:

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

This prints emails to the console instead of sending them.

### 3. Environment Variables (Recommended)

For security, store sensitive information in environment variables:

```python
import os

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@example.com")
```

Then set environment variables:

```bash
export EMAIL_HOST=smtp.gmail.com
export EMAIL_PORT=587
export EMAIL_HOST_USER=your-email@gmail.com
export EMAIL_HOST_PASSWORD=your-app-specific-password
export DEFAULT_FROM_EMAIL=noreply@example.com
```

Or in `.env` file (with python-dotenv):

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@example.com
```

## How It Works

### Signal Handler

When an Order is created, Django signals automatically trigger email sending:

1. **Order Confirmation Email** - Always sent

   - Includes order ID, date, and items ordered
   - Shows delivery address
   - Contains next steps information
   - Template: `project/templates/project/emails/order_confirmation.html`

2. **Donation Thank You Email** - Only if donation_amount > 0
   - Thanks customer for donation
   - Explains impact of donation
   - Shows donation amount
   - Template: `project/templates/project/emails/donation_thank_you.html`

### Email Templates

Located in `project/templates/project/emails/`:

- `order_confirmation.html` - HTML version of order confirmation
- `order_confirmation.txt` - Plain text version
- `donation_thank_you.html` - HTML version of donation thank you
- `donation_thank_you.txt` - Plain text version

## Testing

### Test Email Configuration

```bash
python manage.py shell
```

Then in the Python shell:

```python
from django.core.mail import send_mail

send_mail(
    "Test Subject",
    "Test message body",
    "from@example.com",
    ["to@example.com"],
    fail_silently=False,
)
```

### View Sent Emails in Console (Development)

```python
# In settings.py
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

### Send Test Order Email

```python
from project.models import Order
from project.utils import send_order_confirmation_email

order = Order.objects.first()
send_order_confirmation_email(order)
```

## Troubleshooting

### "SMTP authentication failed"

- Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- Verify the credentials are correct
- For Gmail, ensure you're using an App Password, not your regular password

### "Connection refused" or timeout

- Verify EMAIL_HOST and EMAIL_PORT are correct
- Check firewall settings
- Ensure EMAIL_USE_TLS/EMAIL_USE_SSL matches the provider

### Emails not being sent

- Check EMAIL_BACKEND is set correctly
- Verify DEFAULT_FROM_EMAIL is set
- Check Django logs for errors
- Use console backend to see if emails are being generated

### HTML Not Displaying in Email Client

- Some email clients don't support CSS well
- Check the email in different clients
- Consider using inline CSS or email-specific CSS frameworks

## Additional Configuration

### Email Rate Limiting

If using a service with rate limits, consider adding delay:

```python
# In utils.py, modify send_order_confirmation_email
import time

time.sleep(0.5)  # Add 500ms delay between emails
```

### Async Email Sending

For better performance, use Celery for async email:

```bash
pip install celery django-celery-beat
```

## Security Best Practices

1. **Never commit credentials** - Use environment variables
2. **Use app-specific passwords** - Don't use your main account password
3. **Enable TLS/SSL** - Always encrypt email transmission
4. **Monitor email logs** - Track sent/failed emails
5. **Test with console backend first** - Before going live

## Support

For issues or questions:

- Check Django email documentation: https://docs.djangoproject.com/en/stable/topics/email/
- Verify your email provider's SMTP settings
- Check application logs for detailed error messages
