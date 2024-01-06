CATEGORY_CHOICES = [
    ('Burger', 'Burger'),
    ('Pizza', 'Pizza'),
    ('Chicken', 'Chicken'),
    ('Fish', 'Fish'),
    ('Pie', 'Pie'),
    ('Asian', 'Asian'),
    ('Desserts', 'Desserts'),
    ('Skewers', 'Skewers'),
    ('Rice', 'Rice'),
    ('Vegetables', 'Vegetables'),
    ('Other', 'Other'),
]

ESTIMATED_ARRIVAL_CHOICES = [(i, f'{i} minutes') for i in range(20, 91)]
ONGOING = 'Ongoing'
COMPLETED = 'Completed'
STATUS_CHOICES = [
    (ONGOING, 'Ongoing'),
    (COMPLETED, 'Completed'),
]