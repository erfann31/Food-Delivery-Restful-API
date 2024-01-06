import random


def generate_random_stars():
    return round(random.uniform(1, 5), 1)


def generate_random_stars_count():
    return random.randint(5, 1000)


def generate_random_delivery_times():
    min_time = random.randint(15, 75)
    max_time = random.randint(min_time + 15, 90)
    return min_time, max_time
