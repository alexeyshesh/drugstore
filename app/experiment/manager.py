from datetime import date, timedelta

from app.ctl.orders import OrdersController
from app.ctl.storage import StorageController
from app.exceptions import BadExperimentDateRange

from app.experiment.config import ExperimentConfig


class ExperimentManager:

    orders_ctl = OrdersController()
    storage_ctl = StorageController()
    logs = []  # type: list[dict]

    def __init__(
        self,
        medicines: list[dict],
        margin: float,
        couriers_amount: int,
        expiration_discount_days: int = 30,
        expiration_discount: float = 0.5,
    ):
        exp_conf = ExperimentConfig()
        exp_conf.medicines = medicines
        exp_conf.margin = margin
        exp_conf.couriers_amount = couriers_amount
        exp_conf.expiration_discount_days = expiration_discount_days
        exp_conf.expiration_discount = expiration_discount

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
