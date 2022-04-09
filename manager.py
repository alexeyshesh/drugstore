from datetime import date, timedelta

from app.experiment.manager import ExperimentManager

mngr = ExperimentManager.from_yaml('/Users/alexeyshesh/exp.yaml')
mngr.run(date.today(), date.today() + timedelta(90))
