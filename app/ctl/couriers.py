from app.models.courier import Courier

from app.ctl.base import BaseController


class CouriersController(BaseController):

    couriers = []

    def __init__(self, couriers: list[Courier] = None):
        if couriers is not None:
            self.couriers = couriers
