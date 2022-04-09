from datetime import date

from app.ctl.storage import StorageController
from app.models.medicine import MedicineItem, Medicine

M1 = Medicine('ношпа', 'NS', 100, 100, '', '')
M2 = Medicine('витаминки', 'VT', 10, 200, '', '')

m1 = MedicineItem(M1, date(2022, 3, 10))
m2 = MedicineItem(M2, date(2022, 4, 4))
m3 = MedicineItem(M2, date(2022, 4, 4))

StorageController().add([m1, m2, m3])

print(StorageController().items)
