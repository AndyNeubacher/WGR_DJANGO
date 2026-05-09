"""
ASGI config for WGR.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WGR.settings')

application = get_asgi_application()
