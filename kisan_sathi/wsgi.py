"""
WSGI config for kisan_sathi project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kisan_sathi.settings')

application = get_wsgi_application()
