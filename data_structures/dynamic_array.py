"""Динамический массив — как устроен list внутри.

Задание: реализуй массив, который растёт сам, поверх массива фиксированного размера.
Внутри можно хранить только список фиксированной длины ([None] * capacity) и
не вызывать у него append / insert / pop.

Требования:
    - append за O(1) амортизированно: при заполнении ёмкость удваивается;
    - __getitem__ / __setitem__ за O(1), IndexError за пределами [0, len);
      поддержка отрицательных индексов как у list (a[-1]);
    - pop() с конца за O(1), IndexError на пустом;
    - insert(i, x) за O(n): элементы справа сдвигаются;
    - __len__, __iter__.

Подумай до кода:
    - Почему ёмкость умножают на 2 (или 1.125 как в CPython), а не прибавляют +10?
      Посчитай суммарную стоимость n append в обоих случаях.
"""

from collections.abc import Iterator
from typing import Any


class DynamicArray:
    def __init__(self, capacity: int = 4) -> None:
        raise NotImplementedError

    @property
    def capacity(self) -> int:
        raise NotImplementedError

    def append(self, value: Any) -> None:
        raise NotImplementedError

    def insert(self, index: int, value: Any) -> None:
        raise NotImplementedError

    def pop(self) -> Any:
        raise NotImplementedError

    def __getitem__(self, index: int) -> Any:
        raise NotImplementedError

    def __setitem__(self, index: int, value: Any) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[Any]:
        raise NotImplementedError
