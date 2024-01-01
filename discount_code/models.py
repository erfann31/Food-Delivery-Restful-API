from django.db import models


class DiscountCode(models.Model):
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    code_text = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code_text} - {self.discount_percent}% Discount"
