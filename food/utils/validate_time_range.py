from django.core.exceptions import ValidationError


def validate_time_range(min_time, max_time):
    if min_time >= max_time or max_time - min_time >= 60:
        raise ValidationError("Invalid time range")
