import secrets

from django.utils import timezone


def generate_verification_token():
    random_string = secrets.token_urlsafe(16)
    timestamp = str(int(timezone.now().timestamp()))
    return f'{random_string}_{timestamp}'


def generate_password_reset_token(user):
    user.password_reset_token_created_at = timezone.now()
    user.save()
    return secrets.token_urlsafe(32)
