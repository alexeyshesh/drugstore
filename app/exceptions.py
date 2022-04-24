class DrugstoreError(Exception):
    pass


class MedicineItemExpiredError(DrugstoreError):
    """
    С просроченным лекарством производятся какие-то действия кроме утилизации
    """
    def __init__(self, medicine_item, cur_date=None):
        super().__init__(
            f'Medicine {medicine_item} expired at {medicine_item.expires_at} (today is {cur_date})',
        )


class MedicineNotFound(DrugstoreError):
    def __init__(self, medicine_item):
        super().__init__(f'There is no {medicine_item} in the storage')


class BadExperimentDateRange(DrugstoreError):
    def __init__(self):
        super().__init__('date_to should be greater than date_from')
