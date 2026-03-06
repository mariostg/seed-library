# This script is for testing the Mailtrap Sandbox SMTP configuration.
# It can be run with `python scripts/sandbox-mail.py` and should send a test email to the specified recipient.

import logging
import os
import sys
from pathlib import Path

import django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
os.chdir(BASE_DIR)
django.setup()

connection = get_connection(
    backend="django.core.mail.backends.smtp.EmailBackend",
    host=settings.EMAIL_HOST,
    port=settings.EMAIL_PORT,
    username=settings.EMAIL_HOST_USER,
    password=settings.EMAIL_HOST_PASSWORD,
    use_tls=settings.EMAIL_USE_TLS,
    use_ssl=settings.EMAIL_USE_SSL,
)

email = EmailMultiAlternatives(
    "It works!!!",
    "This was sent through Mailtrap Sandbox SMTP",
    "Sandbox Sender <hello@mariostg.com>",
    ["mario.stg@videotron.ca"],
    connection=connection,
    headers={"X-MT-Category": "order_cancelled"},
)

sent_count = email.send(fail_silently=False)
logger.info(
    "sent=%s host=%s port=%s tls=%s ssl=%s",
    sent_count,
    settings.EMAIL_HOST,
    settings.EMAIL_PORT,
    settings.EMAIL_USE_TLS,
    settings.EMAIL_USE_SSL,
)

if sent_count < 1:
    logger.error("Email not sent: sent_count=%s", sent_count)
    raise SystemExit(1)
