from django.db import models

from user.models import CustomUser


class Address(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    user = models.ForeignKey(CustomUser, related_name='addresses', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} - {self.zipcode}"
