class DrugstoreError(Exception):
    pass


class MedicineItemExpiredError(DrugstoreError):
    """
    С просроченным лекарством производятся какие-то действия кроме утилизации
    """
    def __init__(self, medicine_item):
        super().__init__(f'Medicine {medicine_item} expired')


class MedicineNotFound(DrugstoreError):
    def __init__(self, medicine_item):
        super().__init__(f'There is no {medicine_item} in the storage')
