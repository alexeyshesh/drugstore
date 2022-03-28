import pytest
from datetime import date, timedelta

from app.ctl.storage import StorageController
from app.models.utils import BarcodeGenerator
from app.models.medicine import MedicineItem, Medicine


@pytest.fixture
def storage_items():
    BarcodeGenerator._clear_cache()

    meds = [
        Medicine('Но-шпа', 'NSH', 100),
        Medicine('Витамин С', 'VTC', 10),
    ]
    items = [
        MedicineItem(meds[0], 100, date(2022, 3, 10)),
        MedicineItem(meds[1], 100, date(2022, 4, 4)),
        MedicineItem(meds[1], 100, date(2022, 4, 4)),
    ]

    return items


def test_storage_add(storage_items):
    s = StorageController()
    s.add(storage_items)

    expected_items = {
        item.barcode: item
        for item in storage_items
    }

    assert s.items == expected_items


def test_storage_pop(storage_items):
    s = StorageController()
    s.add(storage_items)

    expected_items = {
        item.barcode: item
        for item in storage_items
    }

    assert s.items == expected_items


def test_storage_the_same_in_different_instances(storage_items):
    StorageController().add(storage_items)
    StorageController().pop(storage_items[0].barcode)

    expected_items = {
        item.barcode: item
        for item in storage_items[1:]
    }

    assert StorageController().items == expected_items


def test_utilize_expired():
    StorageController.items = {}

    med = Medicine('Но-шпа', 'NSH', 100)

    items = [
        MedicineItem(med, 100, date.today() - timedelta(5)),
        MedicineItem(med, 100, date.today()),
        MedicineItem(med, 100, date.today() + timedelta(5)),
    ]

    s = StorageController()
    s.add(items)
    s.utilize_expired()

    expected_barcodes = set(item.barcode for item in items[1:])
    actual_barcodes = set(s.items.keys())
    assert actual_barcodes == expected_barcodes
