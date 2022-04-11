from datetime import date, timedelta

import eel

from app.ctl.storage import StorageController
from app.experiment.config import ExperimentConfig
from app.experiment.logger import Logger
from app.experiment.manager import ExperimentManager
from app.models.courier import Courier
from app.models.medicine import Medicine


@eel.expose
def start_modeling(data):
    data['margin'] = float(data['margin']) / 100
    data['budget'] = float(data['budget'])
    data['courier_salary'] = float(data['courier_salary'])
    data['expiration_discount'] = float(data['expiration_discount']) / 100
    data['supply_size'] = int(data['supply_size'])
    data['couriers_amount'] = int(data['couriers_amount'])
    data['medicines'] = [
        Medicine(
            name=med['name'],
            code=med['code'],
            retail_price=float(med['retail_price']),
            portion_size=int(med['portion_size']),
            demand_formula=med['demand_price_formula'],
        )
        for med in data['medicines']
    ]
    data['couriers'] = [
        Courier(
            name=f'Курьер {i}',
            working_hours=timedelta(hours=int(data['working_hours'])),
        )
        for i in range(int(data['couriers_amount']))
    ]
    ExperimentManager(**data).run(
        date.fromisoformat(data['date_from']),
        date.fromisoformat(data['date_to']),
        eel.showProgress,
    )
    eel.showResults(
        ExperimentConfig().budget - ExperimentConfig().start_budget,
        Logger().get_delivered_orders_amount(),
        Logger().get_average_waiting_time(),
        StorageController().total_price,
        Logger().logs,
    )


def run():
    eel.init('app/ui/web')
    eel.start('index.html')
