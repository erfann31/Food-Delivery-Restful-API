from django.db import models

from address.models import Address
from user.models import CustomUser


class OrderItem(models.Model):
    food = models.ForeignKey('Food', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.food.name} - Quantity: {self.quantity}"


class Order(models.Model):
    ESTIMATED_ARRIVAL_CHOICES = [(i, f'{i} minutes') for i in range(20, 91)]
    user = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    orderItems = models.ManyToManyField(OrderItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=(('Ongoing', 'Ongoing'), ('Completed', 'Completed')))
    date_and_time = models.DateTimeField(auto_now_add=True)
    delivery_address = models.ForeignKey(Address, related_name='orders', on_delete=models.CASCADE)
    discount_code = models.CharField(max_length=50, blank=True)
    estimated_arrival = models.IntegerField(choices=ESTIMATED_ARRIVAL_CHOICES)
    is_canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"Order ID: {self.pk} - Status: {self.status}"

