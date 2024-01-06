from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from user.utils.token_generator import generate_verification_token
from user.utils.url_generator import get_reset_url, get_verification_url


def send_verification_email(user):
    if not user.verification_token:
        user.verification_token = generate_verification_token()
        user.save()

    subject = 'Verify your email'
    verification_url = get_verification_url(user.verification_token)
    message = render_to_string('verification_email_template.html', {
        'user_name': user.name,
        'verification_url': verification_url
    })
    plain_message = strip_tags(message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=message)


def send_password_reset_email(user):
    subject = 'Password Reset Request'
    reset_url = get_reset_url(user.password_reset_token)
    message = render_to_string('password_reset_email_template.html', {'reset_url': reset_url})
    plain_message = strip_tags(message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=message)
