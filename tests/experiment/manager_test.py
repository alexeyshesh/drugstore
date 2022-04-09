from datetime import timedelta

from mock import MagicMock, Mock, patch

from app.experiment.manager import ExperimentManager
from app.models.courier import Courier
from app.models.medicine import Medicine


class FakeExperimentManager(ExperimentManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inited_with = kwargs


@patch('app.experiment.manager.open', MagicMock())
def test_manager_from_yaml():
    data = {
        'medicines': {
            'Ношпа': {
                'code': 'NSP',
                'portion_size': 100,
                'retail_price': 100,
            },
        },
        'couriers': {
            'Иван': {
                'working_hours': 4,
            },
        },
        'margin': 0.1,
    }

    with patch('app.experiment.manager.yaml.safe_load', Mock(return_value=data)):
        mngr = FakeExperimentManager.from_yaml('', expiration_discount=0.2, expiration_discount_days=20)

    expected_init_data = {
        'medicines': [
            Medicine(code='NSP', name='Ношпа', retail_price=100, portion_size=100),
        ],
        'couriers': [
            Courier(name='Иван', working_hours=timedelta(hours=4)),
        ],
        'margin': 0.1,
        'expiration_discount': 0.2,
        'expiration_discount_days': 20,
    }

    assert mngr.inited_with == expected_init_data
