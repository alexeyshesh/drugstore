from datetime import date, timedelta

import yaml

from app.ctl.couriers import CouriersController
from app.ctl.orders import OrdersController
from app.ctl.storage import StorageController
from app.exceptions import BadExperimentDateRange
from app.models.medicine import Medicine
from app.models.courier import Courier

from app.experiment.config import ExperimentConfig


class ExperimentManager:

    orders_ctl = OrdersController()
    storage_ctl = StorageController()
    logs = []  # type: list[dict]

    def __init__(
        self,
        medicines: list[Medicine],
        couriers: list[Courier],
        margin: float,
        expiration_discount_days: int = 30,
        expiration_discount: float = 0.5,
    ):
        exp_conf = ExperimentConfig()
        exp_conf.medicines = medicines
        exp_conf.margin = margin
        exp_conf.expiration_discount_days = expiration_discount_days
        exp_conf.expiration_discount = expiration_discount

        CouriersController().couriers = couriers

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
        )

    def run(self, date_from: date, date_to: date):
        if date_from > date_to:
            raise BadExperimentDateRange()

        ExperimentConfig().cur_date = date_from
        for _ in range((date_to - date_from).days):
            self._run_day()
            ExperimentConfig().cur_date += timedelta(1)

    def _run_day(self):
        self.storage_ctl.utilize_expired()
        self.storage_ctl.accept_items_from_provider()
        self.orders_ctl.distribute_orders_to_couriers()

        self.orders_ctl.accept_new_orders()
        self.orders_ctl.make_new_requests()
