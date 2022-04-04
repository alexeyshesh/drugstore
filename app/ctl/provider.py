from datetime import date

from app.models.medicine import MedicineItem

from app.ctl.base import BaseController


class ProviderController(BaseController):

    supply_queue = {}  # type: dict[date, list[MedicineItem]]

    def get_supply(self, date_: date) -> list[MedicineItem]:
        return self.supply_queue.pop(date_)

    def request(self, medicines: dict):
        pass
