from datetime import date, datetime, time, timedelta
from random import randint
from typing import Callable

import yaml

from app.ctl.couriers import CouriersController
from app.ctl.orders import OrdersController
from app.ctl.provider import ProviderController
from app.ctl.storage import StorageController
from app.exceptions import BadExperimentDateRange
from app.experiment.logger import Logger
from app.factories.customer import CustomerFactory
from app.models.medicine import Medicine
from app.models.courier import Courier

from app.experiment.config import ExperimentConfig
from app.experiment.utils import shuffle, random_split
from app.models.order import Order, OrderedItem


class ExperimentManager:

    orders_ctl = OrdersController()
    storage_ctl = StorageController()
    logs = []  # type: list[dict]

    def __init__(
        self,
        medicines: list[Medicine],
        couriers: list[Courier],
        margin: float,
        date_to: date,
        courier_salary: float,
        expiration_discount_days: int = 30,
        expiration_discount: float = 0.5,
        budget: float = 0,
        supply_size: int = 100,
        **kwargs,
    ):
        exp_conf = ExperimentConfig()

        exp_conf.medicines = medicines
        for med in medicines:
            exp_conf.code_to_medicine[med.code] = med

        exp_conf.margin = margin
        exp_conf.budget = budget
        exp_conf.start_budget = budget
        exp_conf.courier_salary = courier_salary
        exp_conf.expiration_discount_days = expiration_discount_days
        exp_conf.expiration_discount = expiration_discount
        exp_conf.cur_date = date.today()
        exp_conf.supply_size = supply_size
        exp_conf.date_to = date_to

        CouriersController().couriers = couriers

        Logger().reset()
        StorageController().reset()
        ProviderController().reset()

    @classmethod
    def from_yaml(
        cls,
        filename: str,
        margin: float = None,
        expiration_discount_days: int = None,
        expiration_discount: float = None,
    ):
        with open(filename, 'r') as f:
            try:
                config_dict = yaml.safe_load(f)
            except yaml.YAMLError:
                raise

        medicines = [
            Medicine(name=med_name, **med_params)
            for med_name, med_params in config_dict.get('medicines', {}).items()
        ]
        couriers = [
            Courier(name=courier_name, working_hours=timedelta(hours=courier_params['working_hours']))
            for courier_name, courier_params in config_dict.get('couriers', {}).items()
        ]
        margin = config_dict.get('margin', margin)
        date_to = config_dict.get('date_to')
        budget = config_dict.get('budget', 0)
        courier_salary = config_dict.get('courier_salary', 0)
        supply_size = config_dict.get('supply_size', 100)
        expiration_discount_days = config_dict.get(
            'expiration_discount_days',
            expiration_discount_days,
        )
        expiration_discount = config_dict.get(
            'expiration_discount',
            expiration_discount,
        )

        return cls(
            medicines=medicines,
            couriers=couriers,
            margin=margin,
            expiration_discount_days=expiration_discount_days,
            expiration_discount=expiration_discount,
            budget=budget,
            supply_size=supply_size,
            courier_salary=courier_salary,
            date_to=date_to,
        )

    def run(
        self,
        date_from: date,
        date_to: date,
        progress_callback: Callable = (lambda x: print(f'Progress: {x}%')),
    ):
        if date_from > date_to:
            raise BadExperimentDateRange()

        ExperimentConfig().cur_date = date_from
        period_len = (date_to - date_from).days

        for i in range(period_len):
            progress_callback(int(i * 100 / period_len))
            self.run_day()

    def run_day(self):
        StorageController().utilize_expired()
        StorageController().accept_items_from_provider()
        OrdersController().distribute_orders_to_couriers()

        if ExperimentConfig().cur_date.day == ExperimentConfig().courier_salary_day:
            CouriersController().pay_salary()

        self.create_new_orders()
        OrdersController().make_new_requests()

        ExperimentConfig().cur_date += timedelta(1)

    def create_new_orders(self):
        max_delivery_time_minutes = max(
            [
                int(courier.working_hours.seconds / 60)
                for courier in CouriersController().couriers
            ],
        )

        new_ordered_meds = []
        for med in ExperimentConfig().medicines:
            med: Medicine
            # ???????????????????? ???????????????????? ???????????????? ?????????????????????? ???? ???????????????? ????????-??????????
            # ?? ???????????????????? ???? ?????????????????? ????????-?? ???? 0.8 ???? 1.2
            new_ordered_meds_amount = int(
                eval(
                    med.demand_formula,
                    {'price': med.retail_price * (1 + ExperimentConfig().margin)},
                ) * (randint(8, 12) / 10),
            )
            new_ordered_meds.extend([med for _ in range(new_ordered_meds_amount)])

        shuffle(new_ordered_meds)
        customers_amount = int(len(new_ordered_meds) / randint(3, 6))
        split_orders = random_split(new_ordered_meds, customers_amount)

        new_orders = []
        new_ordered_items = []
        for raw_order in split_orders:
            order = Order(
                delivery_time=timedelta(minutes=randint(15, max_delivery_time_minutes)),
                ordered_at=datetime.combine(ExperimentConfig().cur_date, time(hour=randint(10, 22))),
                total_price=0,
                customer=CustomerFactory(),
            )
            for med in raw_order:
                new_ordered_items.append(OrderedItem(med, order))
                order.total_price += med.retail_price * (1 + ExperimentConfig().margin)

            Logger().add(
                f'{order.customer.first_name} {order.customer.last_name}'
                f' ?????????????? {", ".join(med.name for med in raw_order)} ???? ?????????? {order.total_price:.2f} ????????????',
                profit=order.total_price,
            )
            ExperimentConfig().budget += order.total_price

            new_orders.append(order)

        OrdersController().orders_queue.extend(new_orders)
        OrdersController().ordered_items.extend(new_ordered_items)
