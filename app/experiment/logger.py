from collections import defaultdict

from app.experiment.config import ExperimentConfig


class Logger:
    __instance = None
    _logs = defaultdict(list)

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def add(self, msg: str = '', tag: str = '', profit: float = 0, loss: float = 0, hidden=False, meta=None):
        self._logs[ExperimentConfig().cur_date].append(
            {
                'msg': msg,
                'tag': tag,
                'profit': profit or -loss,
                'meta': meta or {},
                'hidden': hidden,
            },
        )

    @property
    def logs(self) -> list:
        result = []
        for date in sorted(self._logs.keys()):
            result.append(
                {
                    'date': date.strftime('%d.%m.%Y'),
                    'logs': [lg for lg in self._logs[date] if not lg['hidden']],
                },
            )
        return result

    @property
    def last_day_log(self):
        last_date = max(self._logs.keys())
        return [
            {
                'date': last_date.strftime('%d.%m.%Y'),
                'logs': [lg for lg in self._logs[last_date] if not lg['hidden']],
            },
        ]

    def get_average_waiting_time(self):
        _data = []
        for day in self._logs.values():
            _data.extend([log['meta']['wait_time'] for log in day if 'wait_time' in log['meta']])
        return int(round(sum(_data) / (len(_data) or 1)))

    def get_delivered_orders_amount(self):
        _data = []
        for day in self._logs.values():
            _data.extend([log['meta']['wait_time'] for log in day if 'wait_time' in log['meta']])
        return len(_data)

    def reset(self):
        self._logs.clear()

    def get_average_couriers_load(self) -> float:
        _data = []
        for day in self._logs.values():
            _data.extend([log['meta']['courier_load'] for log in day if log['tag'] == 'courier_load'])
        return sum(_data) / len(_data) if _data else -1

    def get_money_lost_from_utilization(self):
        _data = []
        for day in self._logs.values():
            _data.extend([log['profit'] for log in day if log['tag'] == 'utilization'])
        return sum(_data)
