import random


def generate_random_stars():
    return round(random.uniform(1, 5), 1)


def generate_random_stars_count():
    return random.randint(1, 1000000)


def generate_random_distance():
    return round(random.uniform(0.1, 5), 2)
