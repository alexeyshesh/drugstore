from dataclasses import dataclass
from datetime import date, timedelta

from app import config
from app.exceptions import MedicineItemExpiredError

from app.models.utils import BarcodeGenerator


@dataclass
class Medicine:
    name: str
    code: str
    portion_size: int
    group: str = ''
    type: str = ''


@dataclass
class MedicineItem:
    medicine: Medicine
    retail_price: float
    expires_at: date

    def __post_init__(self):
        self.barcode = BarcodeGenerator.generate(self)

    @property
    def price(self):
        if date.today() > self.expires_at:
            raise MedicineItemExpiredError(self)
        if date.today() + timedelta(config.EXPIRATION_DISCOUNT_TIMEDELTA) >= self.expires_at:
            return self.retail_price / 2
        return self.retail_price

    def __str__(self):
        return f'{self.medicine.name} [{self.barcode}]'
