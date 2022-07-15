from random import randint
from faker import Faker


class DataGenerator:

    faker = Faker()

    @staticmethod
    def generate_big_id() -> int:
        return randint(1000000, 10000000)

