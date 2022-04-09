from datetime import date, timedelta

from app.ctl.storage import StorageController

from app.models.medicine import MedicineItem, Medicine


def test_storage_add(storage_items):
    s = StorageController()
    s.items = {}
    s.add(storage_items)

    expected_items = {
        item.barcode: item
        for item in storage_items
    }

    assert s.items == expected_items


def test_storage_pop(storage_items):
    s = StorageController()
    s.items = {}
    s.add(storage_items)

    expected_items = {
        item.barcode: item
        for item in storage_items
    }

    assert s.items == expected_items


def test_storage_the_same_in_different_instances(storage_items):
    StorageController().items = {}

    StorageController().add(storage_items)
    StorageController().pop(storage_items[0].barcode)

    expected_items = {
        item.barcode: item
        for item in storage_items[1:]
    }

    print(StorageController().items)

    assert StorageController().items == expected_items


def test_utilize_expired():
    StorageController().items = {}

    med = Medicine('Но-шпа', 'NSH', 100, 100)

    items = [
        MedicineItem(med, date.today() - timedelta(5)),
        MedicineItem(med, date.today()),
        MedicineItem(med, date.today() + timedelta(5)),
    ]

    s = StorageController()
    s.add(items)
    s.utilize_expired()

    expected_barcodes = set(item.barcode for item in items[1:])
    actual_barcodes = set(s.items.keys())
    assert actual_barcodes == expected_barcodes


def test_amount_of_medicine_in_stock():
    StorageController().items = {}

    med = Medicine('Но-шпа', 'NSH', 100, 100)

    items = [
        MedicineItem(med, date.today() + timedelta(5)),
        MedicineItem(med, date.today()),
        MedicineItem(med, date.today() + timedelta(5)),
    ]

    s = StorageController()
    s.add(items)

    assert s.amount_of_medicine_in_stock(med.code) == len(items)
