# Моделирование службы доставки лекарств

Приложение для моделирования работы службы доставки лекарств. Среди доступных параметров моделирования:
- Стартовый капитал
- Процент наценки
- Скидка на просроченные товары
- Объем поставок
- Количество курьеров, их рабочие часы и зарплата

## Установка

### Linux / macOS

```shell
git clone git@github.com:alexeyshesh/drugstore.git
cd drugstore
make install
```

### Windows

```shell
git clone git@github.com:alexeyshesh/drugstore.git
cd drugstore
make winstall
```

## Запуск

### Linux / macOS

```shell
make run
```

### Windows

```shell
make wrun
```

## Запуск тестов

```shell
make flake
make tests
```
