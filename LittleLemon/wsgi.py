"""WSGI config for the Little Lemon project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LittleLemon.settings")

application = get_wsgi_application()
