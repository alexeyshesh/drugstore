from random import randint
from datetime import date, timedelta

from app.models.medicine import MedicineItem

from app.factories.base import BaseFactory


class MedicineItemFactory(BaseFactory):
    model = MedicineItem

    portion_size = 100
    group = ''
    type = ''
    retail_price = (lambda: float(randint(100, 500)))
    expires_at = (lambda: date.today() + timedelta(randint(5, 20)))
