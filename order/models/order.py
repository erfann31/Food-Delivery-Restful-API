import random

from django.db import models

from address.models.address import Address
from discount_code.models.discount_code import DiscountCode
from user.models import CustomUser


class Order(models.Model):
    ESTIMATED_ARRIVAL_CHOICES = [(i, f'{i} minutes') for i in range(20, 91)]
    ONGOING = 'Ongoing'
    COMPLETED = 'Completed'
    STATUS_CHOICES = [
        (ONGOING, 'Ongoing'),
        (COMPLETED, 'Completed'),
    ]

    user = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ONGOING)
    date_and_time = models.DateTimeField(auto_now_add=True)
    delivery_address = models.ForeignKey(Address, related_name='orders', on_delete=models.CASCADE)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_arrival = models.IntegerField(choices=ESTIMATED_ARRIVAL_CHOICES)
    is_canceled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.estimated_arrival:
            self.estimated_arrival = random.choice([i for i, _ in self.ESTIMATED_ARRIVAL_CHOICES])
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order ID: {self.pk} - Status: {self.status}"

