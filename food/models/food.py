from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from consts.constants import CATEGORY_CHOICES
from food.utils.save_food_utility import generate_random_delivery_times, generate_random_stars_count, generate_random_stars
from food.utils.validate_time_range import validate_time_range
from restaurant.models.restaurant import Restaurant


class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0),])
    stars = models.FloatField(default=0, validators=[MinValueValidator(1),
                                                                      MaxValueValidator(5)])
    stars_count = models.IntegerField(default=0, validators=[MinValueValidator(1),
                                                                      MaxValueValidator(1000)])
    min_time_to_delivery = models.IntegerField(default=0, validators=[MinValueValidator(15),
                                                                      MaxValueValidator(75)])
    max_time_to_delivery = models.IntegerField(default=0, validators=[MinValueValidator(30),
                                                                      MaxValueValidator(90)])
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.stars:
            self.stars = generate_random_stars()

        if not self.stars_count:
            self.stars_count = generate_random_stars_count()

        if not self.min_time_to_delivery or not self.max_time_to_delivery:
            min_time, max_time = generate_random_delivery_times()
            self.min_time_to_delivery = min_time
            self.max_time_to_delivery = max_time

        validate_time_range(self.min_time_to_delivery, self.max_time_to_delivery)

        super(Food, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
