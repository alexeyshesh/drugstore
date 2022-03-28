from datetime import date

from app.exceptions import MedicineNotFound
from app.models.medicine import MedicineItem


class StorageController:

    items = {}  # type: dict[str: MedicineItem]

    def add(self, items: list[MedicineItem]):
        for item in items:
            self.items[item.barcode] = item

    def pop(self, barcode: str):
        if barcode not in self.items:
            raise MedicineNotFound(barcode)
        return self.items.pop(barcode)

    def utilize_expired(self):
        not_expired = {}
        for barcode, item in self.items.items():
            if item.expires_at >= date.today():
                not_expired[barcode] = item
        self.items = not_expired
