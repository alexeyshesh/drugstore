from app.ctl.provider import ProviderController
from app.models.order import (
    Order,
    OrderedItem,
    RegularOrderedMedicineItem,
)

from app.ctl.base import BaseController
from app.ctl.couriers import CouriersController
from app.ctl.storage import StorageController


class OrdersController(BaseController):

    orders_queue: list[Order] = []
    ordered_items: list[OrderedItem] = []
    regular_ordered_items: list[RegularOrderedMedicineItem] = []

    def distribute_orders_to_couriers(self) -> None:
        couriers = CouriersController().couriers
        for courier in couriers:
            courier_time_left = courier.working_hours
            orders_to_delete = []
            for order in self.orders_queue:
                if self.order_in_stock(order) and courier_time_left >= order.delivery_time:
                    courier_time_left -= order.delivery_time
                    self.ordered_items = [item for item in self.ordered_items if item.order != order]
                    orders_to_delete.append(order)

            for order in orders_to_delete:
                self.orders_queue.remove(order)  # потому что процесс доставки/приемки не моделируется

    def order_in_stock(self, order: Order) -> bool:
        ordered_items = self.get_ordered_items_by_order(order)
        storage = StorageController()
        medicines_in_order = {}

        for item in ordered_items:
            code = item.medicine.code
            if code in medicines_in_order:
                medicines_in_order[code] += 1
            else:
                medicines_in_order[code] = 1

        for code in medicines_in_order:
            if storage.amount_of_medicine_in_stock(code) < medicines_in_order[code]:
                return False
        return True

    def get_ordered_items_by_order(self, order: Order) -> list[OrderedItem]:
        return [
            item for item
            in self.ordered_items
            if item.order == order
        ]

    def accept_new_orders(self):
        """
        Здесь будет модельная функция для генерации новых заказов
        Возможно, она должна быть в ExperimentController
        """
        pass

    def make_new_requests(self) -> None:
        """
        Смотрит, каких лекарств из очереди нет на складе и создает заказы поставщику
        """
        storage = StorageController()
        medicines_in_queue = {}  # {код_лекарства: количество}
        medicines_to_request = {}  # {код_лекарства: количество}
        for ordered_item in self.ordered_items:
            code = ordered_item.medicine.code
            if code in medicines_in_queue:
                medicines_in_queue[code] += 1
            else:
                medicines_in_queue[code] = 1

        for code in medicines_in_queue:
            medicines_in_stock = storage.amount_of_medicine_in_stock(code)
            if medicines_in_stock < medicines_in_queue[code]:
                medicines_to_request[code] = medicines_in_queue[code] - medicines_in_stock

        ProviderController().request(medicines_to_request)
