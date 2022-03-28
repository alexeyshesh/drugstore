class BarcodeGenerator:

    __cache = {}

    @classmethod
    def generate(cls, item):
        if item.medicine.name not in cls.__cache:
            cls.__cache[item.medicine.name] = 0
        cls.__cache[item.medicine.name] += 1
        return f'{item.medicine.code.upper()}-{cls.__cache[item.medicine.name]:04d}'

    @classmethod
    def _clear_cache(cls):
        cls.__cache = {}
