import random

from django.core.exceptions import ValidationError
from django.db import models

from restaurant.models.restaurant import Restaurant, CATEGORY_CHOICES


class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stars = models.FloatField(default=0)
    stars_count = models.IntegerField(default=0)
    min_time_to_delivery = models.IntegerField(default=0)
    max_time_to_delivery = models.IntegerField(default=0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.stars:
            self.stars = round(random.uniform(1, 5), 1)

        if not self.stars_count:
            self.stars_count = random.randint(5, 1000)

        if not self.min_time_to_delivery:
            self.min_time_to_delivery = random.randint(15, 75)  # Random between 15 and 75

        if not self.max_time_to_delivery:
            self.max_time_to_delivery = random.randint(self.min_time_to_delivery + 15, 90)  # Random between min+15 and 90

        if self.min_time_to_delivery >= self.max_time_to_delivery or self.max_time_to_delivery - self.min_time_to_delivery >= 60:
            raise ValidationError("Invalid time range")

        super(Food, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
