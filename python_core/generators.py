"""Генераторы и итераторы.     [неделя 1]

ИНТУИЦИЯ: список — это готовый торт целиком, генератор — повар, который выдаёт
по куску по требованию. Память O(1) вместо O(n): так читают файлы на гигабайты и
подают батчи в обучение модели.

КАК РАБОТАЕТ
    def gen():          g = gen()      # код ещё не выполнялся!
        yield 1         next(g) -> 1   # выполнился до первого yield и замер
        yield 2         next(g) -> 2   # продолжил с места остановки
                        next(g) -> StopIteration
    Протокол: iter(obj) вызывает obj.__iter__() и получает итератор;
    next(it) вызывает it.__next__(); конец — исключение StopIteration.

ТЕРМИНЫ: iterable (можно обойти много раз, например list) против iterator
(одноразовый, хранит позицию), ленивые вычисления, yield from.
ЛОВУШКА: генератор исчерпывается — второй list(g) вернёт [].
"""

from collections import deque
from collections.abc import Iterable, Iterator
from typing import Any


def fibonacci() -> Iterator[int]:
    """Бесконечный генератор чисел Фибоначчи: 0, 1, 1, 2, 3, 5, ...

    >>> from itertools import islice
    >>> list(islice(fibonacci(), 6))
    [0, 1, 1, 2, 3, 5]
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def powers(base: int, n: int) -> Iterator[int]:
    """Первые n степеней числа: base**0, base**1, ..., base**(n-1). Без **, только умножение.

    >>> list(powers(2, 5))
    [1, 2, 4, 8, 16]
    """
    value = 1
    for _ in range(n):
        yield value
        value *= base


def take(iterable: Iterable[Any], n: int) -> list[Any]:
    """Первые n элементов любого итерируемого объекта (в том числе бесконечного).
    Без itertools.islice.

    >>> take(fibonacci(), 3)
    [0, 1, 1]
    """
    result = []
    if n <= 0:
        return result
    for item in iterable:
        result.append(item)
        if len(result) == n:  # останавливаемся сами: бесконечный генератор не исчерпать
            break
    return result


def chunked(iterable: Iterable[Any], size: int) -> Iterator[list[Any]]:
    """Разбить на куски по size элементов (последний может быть короче). Ленивая:
    не загружает весь вход в память. Так формируют батчи для модели.

    >>> list(chunked(range(5), 2))
    [[0, 1], [2, 3], [4]]
    """
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def flatten(nested: Iterable[Any]) -> Iterator[Any]:
    """Раскрыть вложенные списки любой глубины. Строки не раскрывать.

    >>> list(flatten([1, [2, [3, "ab"]], 4]))
    [1, 2, 3, 'ab', 4]
    """
    for item in nested:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item)  # делегируем вложенному генератору
        else:
            yield item


def sliding_windows(iterable: Iterable[Any], k: int) -> Iterator[tuple[Any, ...]]:
    """Все окна длины k подряд. Должно работать и для генераторов (без индексации).

    >>> list(sliding_windows([1, 2, 3, 4], 3))
    [(1, 2, 3), (2, 3, 4)]
    """
    window: deque[Any] = deque(maxlen=k)  # maxlen: старые элементы вытесняются сами
    for item in iterable:
        window.append(item)
        if len(window) == k:
            yield tuple(window)


class Countdown:
    """Итерируемый объект: обратный отсчёт от start до 1 включительно.
    Реализуй протокол итерации вручную (__iter__ / __next__), без yield.

    Важно: по одному объекту Countdown можно пройти циклом НЕСКОЛЬКО раз.
    Подумай: чем итерируемый объект (iterable) отличается от итератора (iterator)?

    >>> list(Countdown(3))
    [3, 2, 1]
    """

    def __init__(self, start: int) -> None:
        self.start = start

    def __iter__(self) -> "CountdownIterator":
        # Каждый вызов iter() даёт НОВЫЙ итератор со своим состоянием,
        # поэтому повторный цикл начинается заново.
        return CountdownIterator(self.start)


class CountdownIterator:
    """Итератор для Countdown: хранит текущее состояние обхода."""

    def __init__(self, current: int) -> None:
        self.current = current

    def __iter__(self) -> "CountdownIterator":
        return self  # итератор тоже итерируем: возвращает сам себя

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value
