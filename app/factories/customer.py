from random import randint

from app.models.customer import Customer

from app.factories.base import BaseFactory

FIRST_NAMES = [
    'Иван',
    'Петр',
    'Василий',
    'Павел',
    'Владимир',
    'Алексей',
    'Антон',
]

SECOND_NAMES = [
    'Петров',
    'Иванов',
    'Сергеев',
    'Гаврилов',
    'Дубровский',
    'Мерзляков',
    'Павлов',
]


class CustomerFactory(BaseFactory):
    model = Customer

    first_name = (lambda: FIRST_NAMES[randint(0, len(FIRST_NAMES) - 1)])
    last_name = (lambda: SECOND_NAMES[randint(0, len(SECOND_NAMES) - 1)])
    phone = '+78005553535'
    address = 'Moscow'
    card = None
