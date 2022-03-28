from datetime import date

from app.exceptions import MedicineNotFound
from app.models.medicine import MedicineItem, Medicine


class StorageController:

    items = {}  # type: dict[str: MedicineItem]

    def add(self, items: list[MedicineItem]):
        for item in items:
            self.items[item.barcode] = item

    def pop(self, barcode: str):
        if barcode not in self.items:
            raise MedicineNotFound(barcode)
        return self.items.pop(barcode)

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
