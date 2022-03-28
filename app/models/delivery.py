from dataclasses import dataclass

from app.models.order import OrderedItem
from app.models.courier import Courier


@dataclass
class DeliveryItem(OrderedItem):
    courier: Courier
    delivered: bool = False
