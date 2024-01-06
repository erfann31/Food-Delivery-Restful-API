import random


def generate_random_stars():
    return round(random.uniform(1, 5), 1)


def generate_random_stars_count():
    return random.randint(500, 10000)


def generate_random_distance():
    return round(random.uniform(0.3, 5), 2)
