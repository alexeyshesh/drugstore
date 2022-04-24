from dataclasses import dataclass
from datetime import date, timedelta
from functools import reduce

from app.exceptions import MedicineItemExpiredError
from app.experiment.config import ExperimentConfig

from app.models.utils import BarcodeGenerator


@dataclass
class Medicine:
    name: str
    code: str
    retail_price: float
    portion_size: int
    demand_formula: str = '-price/5+40'
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
        if ExperimentConfig().cur_date > self.expires_at:
            raise MedicineItemExpiredError(self, ExperimentConfig().cur_date)
        if ExperimentConfig().cur_date + timedelta(ExperimentConfig().expiration_discount_days) >= self.expires_at:
            return reduce(
                lambda x, y: x * y,
                [
                    self.medicine.retail_price,
                    (1 - ExperimentConfig().expiration_discount),
                    1 + ExperimentConfig().margin,
                ],
                1,
            )

        return self.medicine.retail_price * (1 + ExperimentConfig().margin)

    def __str__(self):
        return f'{self.medicine.name} [{self.barcode}]'
