"""
WSGI config for food_delivery project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# User = get_user_model()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')

application = get_wsgi_application()
# users = User.objects.all()
# if not users:
#     User.objects.create_superuser(name="erf", email="erfannasri2@gmail.com", password="123", is_active=True, is_staff=True)
