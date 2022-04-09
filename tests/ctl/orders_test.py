from datetime import timedelta, datetime, date

import mock

from app.models.courier import Courier
from app.models.medicine import Medicine, MedicineItem
from app.models.order import Order, OrderedItem

from app.ctl.couriers import CouriersController
from app.ctl.storage import StorageController
from app.ctl.orders import OrdersController


def test_distribute_orders_to_couriers_with_enough_time_of_courier(storage_items):
    orders_ctl = OrdersController()
    orders_ctl.orders_queue = [
        Order(
            delivery_time=timedelta(minutes=30),
            ordered_at=datetime(2022, 3, 1),
            total_price=1000,
        ),
        Order(
            delivery_time=timedelta(minutes=30),
            ordered_at=datetime(2022, 3, 1),
            total_price=1000,
        ),
    ]

    couriers_ctl = CouriersController()
    couriers_ctl.couriers = [Courier('Ivan', timedelta(hours=2))]

    orders_ctl.distribute_orders_to_couriers()
    assert len(orders_ctl.orders_queue) == 0


def test_distribute_orders_to_couriers_with_not_enough_time_of_courier(storage_items):
    orders_ctl = OrdersController()
    orders_ctl.orders_queue = [
        Order(
            delivery_time=timedelta(minutes=100),
            ordered_at=datetime(2022, 3, 1),
            total_price=1000,
        ),
        Order(
            delivery_time=timedelta(minutes=100),
            ordered_at=datetime(2022, 3, 1),
            total_price=1000,
        ),
    ]

    couriers_ctl = CouriersController()
    couriers_ctl.couriers = [Courier('Ivan', timedelta(hours=2))]

    orders_ctl.distribute_orders_to_couriers()
    assert len(orders_ctl.orders_queue) == 1


def test_distribute_orders_to_couriers_with_enough_time_of_many_couriers(storage_items):
    orders_ctl = OrdersController()
    orders_ctl.orders_queue = [
        Order(
            delivery_time=timedelta(minutes=100),
            ordered_at=datetime(2022, 3, 1),
            total_price=1000,
        ),
        Order(
            delivery_time=timedelta(minutes=100),
            ordered_at=datetime(2022, 3, 1),
            total_price=1000,
        ),
    ]

    couriers_ctl = CouriersController()
    couriers_ctl.couriers = [
        Courier('Ivan', timedelta(hours=2)),
        Courier('Petr', timedelta(hours=2)),
    ]

    orders_ctl.distribute_orders_to_couriers()
    assert len(orders_ctl.orders_queue) == 0


def test_order_in_stock():
    meds = [
        Medicine('foo', 'foo', 100, 10),
        Medicine('bar', 'bar', 200, 9),
        Medicine('xyz', 'xyz', 300, 8),
    ]

    med_items = [
        MedicineItem(meds[0], date.today() + timedelta(100)),
        MedicineItem(meds[0], date.today() + timedelta(100)),
        MedicineItem(meds[1], date.today() + timedelta(100)),
    ]

    storage = StorageController()
    storage.add(med_items)

    orders_ctl = OrdersController()

    # FIXME: возможен баг, вызванный тем, что сравнение разных
    #  экземпляров датакласса происходит по полям

    orders_ctl.orders_queue = [
        Order(timedelta(1), datetime(2022, 1, 1), 1000),
        Order(timedelta(1), datetime(2022, 1, 1), 2000),
        Order(timedelta(1), datetime(2022, 1, 1), 3000),
    ]
    orders_ctl.ordered_items = [
        OrderedItem(meds[0], orders_ctl.orders_queue[0]),
        OrderedItem(meds[1], orders_ctl.orders_queue[0]),

        OrderedItem(meds[1], orders_ctl.orders_queue[1]),
        OrderedItem(meds[1], orders_ctl.orders_queue[1]),
        OrderedItem(meds[0], orders_ctl.orders_queue[1]),

        OrderedItem(meds[0], orders_ctl.orders_queue[2]),
        OrderedItem(meds[1], orders_ctl.orders_queue[2]),
        OrderedItem(meds[2], orders_ctl.orders_queue[2]),
    ]

    assert orders_ctl.order_in_stock(orders_ctl.orders_queue[0])
    assert not orders_ctl.order_in_stock(orders_ctl.orders_queue[1])
    assert not orders_ctl.order_in_stock(orders_ctl.orders_queue[2])


def test_make_new_requests():
    meds = [
        Medicine('foo', 'foo', 100, 10),
        Medicine('bar', 'bar', 100, 9),
        Medicine('xyz', 'xyz', 100, 8),
    ]

    med_items = [
        MedicineItem(meds[0], date.today() + timedelta(100)),
        MedicineItem(meds[0], date.today() + timedelta(100)),
        MedicineItem(meds[1], date.today() + timedelta(100)),
    ]

    storage = StorageController()
    storage.items = {}
    storage.add(med_items)

    orders_ctl = OrdersController()

    orders_ctl.orders_queue = [
        Order(timedelta(1), datetime(2022, 1, 1), 1000),
        Order(timedelta(1), datetime(2022, 1, 1), 2000),
        Order(timedelta(1), datetime(2022, 1, 1), 3000),
    ]
    orders_ctl.ordered_items = [
        OrderedItem(meds[0], orders_ctl.orders_queue[0]),
        OrderedItem(meds[1], orders_ctl.orders_queue[0]),

        OrderedItem(meds[1], orders_ctl.orders_queue[1]),
        OrderedItem(meds[1], orders_ctl.orders_queue[1]),
        OrderedItem(meds[0], orders_ctl.orders_queue[1]),

        OrderedItem(meds[0], orders_ctl.orders_queue[2]),
        OrderedItem(meds[1], orders_ctl.orders_queue[2]),
        OrderedItem(meds[2], orders_ctl.orders_queue[2]),
    ]

    with mock.patch('app.ctl.orders.ProviderController.request') as mocked_provider_request:
        orders_ctl.make_new_requests()
        mocked_provider_request.assert_called_with(
            {
                meds[0].code: 1,
                meds[1].code: 3,
                meds[2].code: 1,
            },
        )
