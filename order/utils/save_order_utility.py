import random

from consts.constants import ESTIMATED_ARRIVAL_CHOICES


def generate_random_estimated_arrival():
    return random.choice([i for i, _ in ESTIMATED_ARRIVAL_CHOICES])
