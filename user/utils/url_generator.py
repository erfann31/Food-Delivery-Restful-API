from django.conf import settings
from django.urls import reverse


def get_verification_url(token):
    return settings.BASE_URL + reverse('email-verification', kwargs={'token': token})


def get_reset_url(token):
    return settings.BASE_URL + reverse('password-reset-confirm', kwargs={'token': token})
