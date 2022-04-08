import pytest
from datetime import date

from app.models.utils import BarcodeGenerator

from app.models.medicine import MedicineItem, Medicine


@pytest.fixture
def storage_items():
    BarcodeGenerator._clear_cache()

    meds = [
        Medicine('Но-шпа', 'NSH', 100, 100),
        Medicine('Витамин С', 'VTC', 200, 10),
    ]
    items = [
        MedicineItem(meds[0], date(2022, 3, 10)),
        MedicineItem(meds[1], date(2022, 4, 4)),
        MedicineItem(meds[1], date(2022, 4, 4)),
    ]

    return items
