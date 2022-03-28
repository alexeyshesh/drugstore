from dataclasses import dataclass
from datetime import datetime

from app.models.customer import Customer
from app.models.medicine import MedicineItem


@dataclass
class Order:
    ordered_at: datetime
    total_price: float


@dataclass
class OrderedItem:
    item: MedicineItem
    order: Order
    customer: Customer


@dataclass
class RegularOrderedMedicineItem:
    item: MedicineItem
    customer: Customer
    repeat_days_period: int
