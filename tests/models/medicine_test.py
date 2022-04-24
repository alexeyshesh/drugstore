from datetime import date, timedelta

from app.experiment.config import ExperimentConfig

from app.models.medicine import Medicine, MedicineItem
from app.models.utils import BarcodeGenerator


def test_discount():
    ExperimentConfig().expiration_discount_days = 10
    price = 100
    med = Medicine('foo', 'bar', 100, 100)
    fresh_item = MedicineItem(
        med,
        date.today() + timedelta(ExperimentConfig().expiration_discount_days + 1),
    )
    old_item = MedicineItem(
        med,
        date.today() + timedelta(ExperimentConfig().expiration_discount_days - 1),
    )

    assert fresh_item.price == price * (1 + ExperimentConfig().margin)
    assert old_item.price == price * (1 - ExperimentConfig().expiration_discount) * (1 + ExperimentConfig().margin)


def test_barcode():
    BarcodeGenerator._clear_cache()
    med = Medicine('foo', 'bar', 100, 100)
    items = [
        MedicineItem(med, date.today() + timedelta(10))
        for _ in range(3)
    ]

    expected_barcodes = ['BAR-0001', 'BAR-0002', 'BAR-0003']
    actual_barcodes = [item.barcode for item in items]

    assert actual_barcodes == expected_barcodes
