class Command:
    """
    `handlers` – список обработчиков команды

    Обработчик принимает один аргумент – событие или команду

    Обработчик возвращает кортеж из двух элементов
    - новые события и команды, которые надо обработать (`list`)
    - произошла ли ошибка во время обработки события (`bool`)

    Если обработка прошла успешно, в очередь добавляются вернувшиеся события
    и команды и обработка продолжается
    Если во время обработки произошла ошибка, выполняются только события и команды,
    вернувшиеся из текущего обработчика, остальные из очереди удаляются
    """
    handlers = []
