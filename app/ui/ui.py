from datetime import date, timedelta

import eel

from app.experiment.manager import ExperimentManager
from app.models.courier import Courier
from app.models.medicine import Medicine


@eel.expose
def start_modeling(data):
    data['margin'] = float(data['margin']) / 100
    data['budget'] = float(data['budget'])
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
    # try:
    ExperimentManager(**data).run(date.today(), date.today() + timedelta(90), eel.showProgress)
    # except Exception as err:
    #     eel.showError(str(err))


def run():
    eel.init('app/ui/web')
    eel.start('index.html')
