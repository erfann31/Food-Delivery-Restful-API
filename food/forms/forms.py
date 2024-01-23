# myapp/forms.py
from django import forms
from django.core.exceptions import ValidationError

from food.models.food import Food
from food.utils.validate_time_range import validate_time_range


class FoodAdminForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        min_time = cleaned_data.get('min_time_to_delivery')
        max_time = cleaned_data.get('max_time_to_delivery')

        try:
            validate_time_range(min_time, max_time)
        except ValidationError as e:
            self.add_error('min_time_to_delivery', e.message)
            self.add_error('max_time_to_delivery', e.message)

        return cleaned_data
