from datetime import date


class ExperimentConfig:

    cur_date: date
    couriers_amount: int
    margin: float
    expiration_discount_days: int = 30
    expiration_discount: float = 0.5
    medicines: list

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        pass