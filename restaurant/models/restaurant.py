from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from consts.constants import CATEGORY_CHOICES, RESTAURANT_TAG_CHOICES
from restaurant.utils.save_restaurant_utility import generate_random_distance, generate_random_stars_count, generate_random_stars


class Restaurant(models.Model):
    header_image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='restaurant_profile_pics/', blank=True, null=True)
    tag1 = models.CharField(max_length=50, choices=RESTAURANT_TAG_CHOICES, blank=True, null=True)
    tag2 = models.CharField(max_length=50, choices=RESTAURANT_TAG_CHOICES, blank=True, null=True)
    stars = models.FloatField(default=0, blank=True, null=True, validators=[MinValueValidator(1),
                                                                            MaxValueValidator(5)])
    stars_count = models.IntegerField(default=0, blank=True, null=True, validators=[MinValueValidator(1), ])
    distance = models.FloatField(default=0, blank=True, null=True, validators=[MinValueValidator(0.1),
                                                                               MaxValueValidator(5)])
    address = models.CharField(max_length=256)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=50)
    courier_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0),
                                                                                               MaxValueValidator(999999)])
    opening_time = models.DecimalField(default=0, max_digits=4, decimal_places=2, validators=[MinValueValidator(0),
                                                                                              MaxValueValidator(24)])

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.stars:
            self.stars = generate_random_stars()

        if not self.stars_count:
            self.stars_count = generate_random_stars_count()

        if not self.distance:
            self.distance = generate_random_distance()

        super(Restaurant, self).save(*args, **kwargs)
