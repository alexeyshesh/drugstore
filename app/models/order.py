from dataclasses import dataclass
from datetime import datetime, timedelta

from app.models.customer import Customer
from app.models.medicine import MedicineItem, Medicine
from app.models.courier import Courier


@dataclass
class Order:
    delivery_time: timedelta
    ordered_at: datetime
    total_price: float
    customer: Customer = None
    courier: Courier or None = None


@dataclass
class OrderedItem:
    medicine: Medicine
    order: Order
    item: MedicineItem = None


@dataclass
class RegularOrderedMedicineItem:
    item: MedicineItem
    customer: Customer
    repeat_days_period: int
