import os
import sys
from pathlib import Path

import dotenv

# 0. Setup

BASE_DIR = Path(__file__).resolve().parent.parent

if "pytest" not in sys.modules:
    dotenv.load_dotenv(dotenv_path=BASE_DIR / ".env")

# 1. Django Core Settings

ALLOWED_HOSTS = ["127.0.0.1"]

DEBUG = os.environ.get("DEBUG", "") == "1"

INSTALLED_APPS = [
    # First Party
    # Third Party
    "debug_toolbar",
    "django_browser_reload",
    # Contrib
]

ROOT_URLCONF = "main.urls"

USE_TZ = True

# 2. Django Contrib Settings

# django.contrib.auth
PASSWORD_HASHERS = "..."

# 3. Third Party Settings

# django-version-checks
VERSION_CHECKS = "..."

# 4. Project Settings

SOME_API_URL = os.environ.get("SOME_API_URL", "...")
PAGE_SIZE = 100
