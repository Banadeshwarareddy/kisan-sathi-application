"""
ASGI config for kisan_sathi project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kisan_sathi.settings')

application = get_asgi_application()
