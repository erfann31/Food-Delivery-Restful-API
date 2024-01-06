import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from food.models.food import Food
from restaurant.models.restaurant import Restaurant


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('Name'), max_length=255)
    email = models.EmailField(_('Email'), unique=True)
    password = models.CharField(_('Password'), max_length=128)
    photo = models.ImageField(_('Photo'), upload_to='user_photos/', blank=True, null=True)
    mobile_number = models.CharField(_('Mobile Number'), max_length=15, blank=True)
    verified = models.BooleanField(_('Verified'), default=False)
    verification_token = models.CharField(_('Verification Token'), max_length=100, blank=True)
    password_reset_token = models.CharField(_('Password Reset Token'), max_length=100, blank=True)
    favorite_foods = models.ManyToManyField(Food, related_name='favorited_by', blank=True)
    favorite_restaurants = models.ManyToManyField(Restaurant, related_name='favorited_by', blank=True)

    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)
    password_reset_token_created_at = models.DateTimeField(null=True, blank=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def send_verification_email(self):
        if not self.verification_token:
            self.verification_token = self.generate_verification_token()
            self.save()

        subject = 'Verify your email'
        verification_url = self.get_verification_url()
        message = render_to_string('verification_email_template.html', {
            'user_name': self.name,
            'verification_url': verification_url
        })
        plain_message = strip_tags(message)
        from_email = settings.EMAIL_HOST_USER
        to = self.email

        send_mail(subject, plain_message, from_email, [to], html_message=message)

    def generate_verification_token(self):
        random_string = secrets.token_urlsafe(16)
        timestamp = str(int(timezone.now().timestamp()))
        return f'{random_string}_{timestamp}'

    def get_verification_url(self):
        return settings.BASE_URL + reverse('email-verification', kwargs={'token': self.verification_token})

    def get_reset_url(self):
        return settings.BASE_URL + reverse('password-reset-confirm', kwargs={'token': self.password_reset_token})

    def verification_token_expired(self):
        expiration_duration = timedelta(minutes=2)
        token_parts = self.verification_token.split('_')
        timestamp = int(token_parts[-1]) if token_parts[-1].isdigit() else 0
        expiration_time = timezone.now() - expiration_duration
        return timestamp < expiration_time.timestamp()

    def generate_password_reset_token(self):
        self.password_reset_token = secrets.token_urlsafe(32)
        self.password_reset_token_created_at = timezone.now()
        self.save()

    def password_reset_token_expired(self):
        expiration_duration = timedelta(minutes=2)
        if not self.password_reset_token_created_at:
            return True
        expiration_time = self.password_reset_token_created_at + expiration_duration
        return expiration_time <= timezone.now()

    def send_password_reset_email(self):
        subject = 'Password Reset Request'
        reset_url = self.get_reset_url()
        message = render_to_string('password_reset_email_template.html', {'reset_url': reset_url})
        plain_message = strip_tags(message)
        from_email = settings.EMAIL_HOST_USER
        to = self.email

        send_mail(subject, plain_message, from_email, [to], html_message=message)
