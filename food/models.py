import random

from django.db import models

from restaurant.models import Restaurant,CATEGORY_CHOICES


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

        super(Food, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
