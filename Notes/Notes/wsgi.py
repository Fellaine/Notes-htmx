"""
WSGI config for Notes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
# from pathlib import Path

# import dotenv

from django.core.wsgi import get_wsgi_application

# BASE_DIR = Path(__file__).resolve().parent.parent
# ENV_FILE_PATH = BASE_DIR / ".env"

# dotenv.read_dotenv(str(ENV_FILE_PATH))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Notes.settings')

application = get_wsgi_application()
