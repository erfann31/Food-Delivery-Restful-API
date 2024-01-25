from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
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
    photo = models.TextField(blank=True,  null=True)
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
        ordering = ['email']
        verbose_name = _('User')
        verbose_name_plural = _('Users')
