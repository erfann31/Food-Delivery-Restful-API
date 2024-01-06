from datetime import timedelta

from django.utils import timezone


def verification_token_expired(token):
    expiration_duration = timedelta(minutes=2)
    token_parts = token.split('_')
    timestamp = int(token_parts[-1]) if token_parts[-1].isdigit() else 0
    expiration_time = timezone.now() - expiration_duration
    return timestamp < expiration_time.timestamp()


def password_reset_token_expired(created_at):
    expiration_duration = timedelta(minutes=2)
    if not created_at:
        return True
    expiration_time = created_at + expiration_duration
    return expiration_time <= timezone.now()
