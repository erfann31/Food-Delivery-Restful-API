import random

from django.core.validators import MaxValueValidator
from django.db import models

from consts.constants import CATEGORY_CHOICES, RESTAURANT_TAG_CHOICES


class Restaurant(models.Model):
    header_image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='restaurant_profile_pics/', blank=True, null=True)
    tag1 = models.CharField(max_length=50, choices=RESTAURANT_TAG_CHOICES, blank=True, null=True)
    tag2 = models.CharField(max_length=50, choices=RESTAURANT_TAG_CHOICES, blank=True, null=True)
    stars = models.FloatField(default=0)
    stars_count = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    address = models.CharField(max_length=256)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=50)
    courier_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    opening_time = models.DecimalField(default=0, max_digits=4, decimal_places=2, validators=[MaxValueValidator(24)])

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.stars:
            self.stars = round(random.uniform(1, 5), 1)

        if not self.stars_count:
            self.stars_count = random.randint(500, 10000)

        if not self.distance:
            self.distance = round(random.uniform(0.3, 5), 2)

        super(Restaurant, self).save(*args, **kwargs)
