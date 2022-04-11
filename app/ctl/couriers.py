from app.experiment.config import ExperimentConfig
from app.experiment.logger import Logger
from app.models.courier import Courier

from app.ctl.base import BaseController


class CouriersController(BaseController):

    couriers = []

    def __init__(self, couriers: list[Courier] = None):
        if couriers is not None:
            self.couriers = couriers

    def pay_salary(self):
        ExperimentConfig().budget -= ExperimentConfig().courier_salary * len(self.couriers)
        Logger().add('Выплата зарплаты курьерам', loss=ExperimentConfig().courier_salary * len(self.couriers))
