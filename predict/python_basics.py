"""Предскажи результат: ловушки Python.     [недели 1–3]

КАК РАБОТАТЬ
    1. Прочитай функцию qNN и, НЕ ЗАПУСКАЯ её, впиши в ANSWERS то, что она вернёт
       (Python-значение: [1, 2], (True, None), "abc" ...).
    2. pytest tests/test_predict.py -k python — тест сравнит твой ответ с реальным.
    3. Ошибся — найди, в каком месте мысленное выполнение разошлось с настоящим.
       Именно эти места спрашивают на интервью.

Такой формат тренирует чтение кода — навык, который нужен на code review и при отладке
чаще, чем написание с нуля.
"""

from collections import defaultdict


def q01():
    """Значение аргумента по умолчанию."""

    def add(item, bucket=[]):  # noqa: B006  (ловушка намеренная)
        bucket.append(item)
        return bucket

    a = add(1)
    b = add(2)
    return a, b, a is b


def q02():
    """Лямбды в цикле."""
    funcs = [lambda: i for i in range(3)]  # noqa: B023
    return [f() for f in funcs]


def q03():
    """Умножение списка списков."""
    grid = [[0] * 3] * 2
    grid[0][0] = 1
    return grid


def q04():
    """Удаление из списка во время обхода."""
    nums = [2, 2, 2, 3]
    for n in nums:
        if n == 2:
            nums.remove(n)
    return nums


def q05():
    """Генератор, пройденный дважды."""
    squares = (x * x for x in range(3))
    first = list(squares)
    second = list(squares)
    return first, second


def q06():
    """Ключи словаря 1, True, 1.0."""
    d = {1: "int", True: "bool", 1.0: "float"}  # noqa: F601
    return d


def q07():
    """+= для списка внутри кортежа."""
    t = ([1],)
    try:
        t[0] += [2]
    except TypeError:
        pass
    return t


def q08():
    """sort против sorted."""
    a = [3, 1, 2]
    b = a.sort()
    return a, b


def q09():
    """Поверхностная копия."""
    a = [[1], [2]]
    b = a.copy()
    b[0].append(9)
    b.append([3])
    return a


def q10():
    """Сравнения."""
    return 1 < 3 > 2, 1 == 1.0 == True, 0.1 + 0.2 == 0.3  # noqa: E712


def q11():
    """Строки неизменяемы."""
    s = "ab"
    t = s
    s += "c"
    return t


def q12():
    """defaultdict и чтение несуществующего ключа."""
    d = defaultdict(int)
    if d["x"] == 0:
        pass
    return len(d)


def q13():
    """Изменяемый атрибут КЛАССА."""

    class Basket:
        items = []  # noqa: RUF012

    a, b = Basket(), Basket()
    a.items.append("apple")
    return b.items


def q14():
    """Деление и округление."""
    return -7 // 2, int(-7 / 2), round(2.5), round(3.5)


def q15():
    """Присваивание переменной из внешней функции без nonlocal."""
    x = 1

    def inc():
        x += 1  # noqa: F823
        return x

    try:
        return inc()
    except Exception as e:
        return type(e).__name__


def q16():
    """Ленивость генератора."""
    log = []

    def gen():
        log.append("start")
        yield 1
        log.append("end")

    it = gen()
    before = list(log)
    next(it)
    after = list(log)
    return before, after


def q17():
    """Распаковка со звёздочкой."""
    *head, last = [1]
    first, *middle, end = [1, 2, 3, 4, 5]  # noqa: F841
    return head, last, middle


def q18():
    """Поиск переменной в момент вызова."""
    x = 10

    def show():
        return x

    x = 20
    return show()


ANSWERS = {
    "q01": ([1, 2], [1, 2], True),  # список по умолчанию создаётся один раз при def
    "q02": [2, 2, 2],  # лямбды запоминают переменную i, а не значение; к вызову i == 2
    "q03": [[1, 0, 0], [1, 0, 0]],  # [row] * 2 — две ссылки на ОДИН список
    "q04": [2, 3],  # после remove элементы сдвигаются, цикл перепрыгивает следующий
    "q05": ([0, 1, 4], []),  # генератор одноразовый, второй проход пустой
    "q06": {1: "float"},  # 1 == True == 1.0 и hash равны: ключ один, значение последнее
    "q07": ([1, 2],),  # список изменился (+= на месте), потом присваивание в кортеж упало
    "q08": ([1, 2, 3], None),  # list.sort() сортирует на месте и возвращает None
    "q09": [[1, 9], [2]],  # copy() копирует внешний список, вложенные — те же объекты
    "q10": (True, True, False),  # цепочки: (1<3) and (3>2); 0.1+0.2 == 0.30000000000000004
    "q11": "ab",  # += создал новую строку и перепривязал s; t указывает на старую
    "q12": 1,  # чтение d["x"] у defaultdict СОЗДАЁТ ключ
    "q13": ["apple"],  # items — атрибут класса, общий для всех экземпляров
    "q14": (-4, -3, 2, 4),  # // округляет вниз; int() к нулю; round — к чётному (банковское)
    "q15": "UnboundLocalError",  # присваивание делает x локальной для inc, а она ещё пуста
    "q16": ([], ["start"]),  # тело генератора не выполняется до первого next()
    "q17": ([], 1, [2, 3, 4]),  # *head забирает «всё остальное», может быть пустым
    "q18": 20,  # замыкание ищет x в момент вызова, а не в момент создания функции
}
