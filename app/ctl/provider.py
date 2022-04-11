from collections import defaultdict
from datetime import date, timedelta
from random import randint

from app.experiment.config import ExperimentConfig
from app.experiment.logger import Logger
from app.models.medicine import MedicineItem

from app.ctl.base import BaseController


class ProviderController(BaseController):

    supply_queue = defaultdict(list)  # type: dict[date, list[MedicineItem]]
    requested_items = defaultdict(int)  # type: dict[str, int]

    def get_supply(self, date_: date) -> list[MedicineItem]:
        return self.supply_queue.get(date_, [])

    def create_supply(self, code):
        supply_date = ExperimentConfig().cur_date + timedelta(randint(1, 10))
        medicine = ExperimentConfig().code_to_medicine[code]
        self.supply_queue[supply_date].extend([
            MedicineItem(
                medicine=medicine,
                expires_at=ExperimentConfig().cur_date + timedelta(30),
            )
            for _ in range(ExperimentConfig().supply_size)
        ])

        Logger().add(
            f'Заказана поставка прерапата {medicine.name} '
            f'на сумму {medicine.retail_price * ExperimentConfig().supply_size} рублей. '
            f'Заказ прибудет на склад {supply_date.strftime("%d.%m.%Y")}',
            loss=medicine.retail_price * ExperimentConfig().supply_size,
        )

    def request(self, medicines: dict[str, int]):
        for code, amount in medicines.items():
            self.requested_items[code] += amount
            if self.requested_items[code] > 0:
                self.create_supply(code)
                self.requested_items[code] -= ExperimentConfig().supply_size
                ExperimentConfig().budget -= (
                    ExperimentConfig().supply_size * ExperimentConfig().code_to_medicine[code].retail_price
                )
