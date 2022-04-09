from random import randint


def shuffle(lst: list):
    tmp_lst = []
    while lst:
        tmp_lst.append(lst.pop(randint(0, len(lst) - 1)))
    lst.extend(tmp_lst)


def random_split(lst: list, parts: int):
    result = []
    splitters = []

    while len(splitters) < parts - 1:
        new_splitter = randint(1, len(lst) - 1)
        if new_splitter not in splitters:
            splitters.append(new_splitter)
    splitters.extend([0, len(lst)])
    splitters.sort()

    for i in range(1, len(splitters)):
        result.append(lst[splitters[i - 1]:splitters[i]])

    return result
