import random
from datetime import datetime, timedelta

def generate_stream(size):
        gen = random_date_generator()
        return [next(gen) for _ in range(size)]

def random_date_generator(start_date = "01-01-2000", end_date = "31-12-2077"):
    start = datetime.strptime(start_date, "%d-%m-%Y")
    end = datetime.strptime(end_date, "%d-%m-%Y")
    delta = (end - start).days

    while True:
        random_days = random.randint(0, delta)
        yield start + timedelta(days=random_days)
