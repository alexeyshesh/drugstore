from dataclasses import dataclass
from datetime import date, timedelta

from app.exceptions import MedicineItemExpiredError
from app.experiment.config import ExperimentConfig

from app.models.utils import BarcodeGenerator


@dataclass
class Medicine:
    name: str
    code: str
    retail_price: float
    portion_size: int
    group: str = ''
    type: str = ''


@dataclass
class MedicineItem:
    medicine: Medicine
    expires_at: date

    def __post_init__(self):
        self.barcode = BarcodeGenerator.generate(self)

    @property
    def price(self):
        if date.today() > self.expires_at:
            raise MedicineItemExpiredError(self)
        if date.today() + timedelta(ExperimentConfig().expiration_discount_days) >= self.expires_at:
            return self.medicine.retail_price * ExperimentConfig().expiration_discount
        return self.medicine.retail_price

    def __str__(self):
        return f'{self.medicine.name} [{self.barcode}]'
