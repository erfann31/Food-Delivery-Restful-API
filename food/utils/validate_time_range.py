from django.core.exceptions import ValidationError


def validate_time_range(min_time, max_time):
    if min_time >= max_time:
        raise ValidationError("Minimum time must be less than maximum time")
    elif max_time - min_time >= 60:
        raise ValidationError("Time range must be less than 60 minutes")
    elif max_time - min_time < 15:
        raise ValidationError("Time range must be at least 15 minutes")
