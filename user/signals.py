from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created and not instance.verified:
        if instance.verification_token:  # Check if the verification token exists
            subject = 'Verify your email'
            html_message = render_to_string('verification_email_template.html', {
                'user_name': instance.name,
                'verification_link': instance.get_verification_url()  # Assuming get_verification_url() generates the verification URL
            })
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER  # Your sender email
            to = instance.email

            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
