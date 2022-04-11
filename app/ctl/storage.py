from datetime import date

from app.ctl.base import BaseController
from app.ctl.provider import ProviderController
from app.exceptions import MedicineNotFound
from app.experiment.config import ExperimentConfig
from app.experiment.logger import Logger
from app.models.medicine import MedicineItem, Medicine


class StorageController(BaseController):

    items = {}  # type: dict[str, MedicineItem]

    def add(self, items: list[MedicineItem]):
        for item in items:
            self.items[item.barcode] = item

    def pop(self, barcode: str) -> MedicineItem:
        if barcode not in self.items:
            raise MedicineNotFound(barcode)
        return self.items.pop(barcode)

    def pop_by_code(self, code: str) -> MedicineItem:
        for barcode, item in self.items.items():
            if item.medicine.code == code:
                return self.pop(barcode)

    def item_in_stock(self, item: MedicineItem) -> bool:
        return item.barcode in self.items

    def medicine_in_stock(self, medicine: Medicine):
        for item in self.items.values():
            if item.medicine == medicine:
                return item.barcode
        return None

    def amount_of_medicine_in_stock(self, medicine_code: str):
        return len([
            item for item
            in self.items.values()
            if item.medicine.code == medicine_code
        ])

    def utilize_expired(self):
        not_expired = {}
        for barcode, item in self.items.items():
            if item.expires_at >= date.today():
                not_expired[barcode] = item
        self.items = not_expired

    def accept_items_from_provider(self):
        provider = ProviderController()
        today = ExperimentConfig().cur_date
        supply = provider.get_supply(today)
        self.add(supply)

        if supply:
            Logger().add(f'От поставщика пришло {len(supply)} штук лекарств!'
                         f' ({", ".join(set([med.medicine.name for med in supply]))})')

    @property
    def total_price(self) -> float:
        return sum(med.price for med in self.items.values())
