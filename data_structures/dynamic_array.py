"""Динамический массив: как устроен list.     [опционально · неделя 1]

ИНТУИЦИЯ
    Ряд кресел в кинотеатре, купленный «с запасом». Пока есть свободные кресла — новый
    гость садится сразу. Кресла кончились — переезжаем в зал вдвое больше и пересаживаем
    всех. Переезд дорогой, но случается всё реже: 4 -> 8 -> 16 -> 32 ...

КАК УСТРОЕНО
    _data:  [10, 20, 30, None, None, None, None, None]    capacity = 8
    _size:  3                                             len = 3
    Элементы лежат подряд, поэтому a[i] — это «начало + i шагов»: O(1).

    append(40): есть место -> _data[3] = 40, _size = 4. O(1).
    append при полном массиве: новый массив 2x, копируем n элементов (O(n)), потом вставка.
    Сумма копирований за n вставок: 1 + 2 + 4 + ... + n < 2n -> O(1) амортизированно.
    insert(0, x): сдвигаем ВСЕ элементы вправо — O(n). Поэтому очередь на list — плохая идея.

ТЕРМИНЫ
    capacity против size, амортизированная сложность, геометрический рост,
    локальность данных (элементы рядом в памяти -> кэш процессора работает хорошо).

ТИПИЧНЫЕ ОШИБКИ
    - расти на +1 или +10 вместо умножения -> n вставок стоят O(n^2);
    - сдвигать при insert слева направо -> затираешь элементы (сдвигай с конца);
    - не обрабатывать отрицательные индексы.

ЗАДАНИЕ: внутри только список фиксированной длины ([None] * capacity),
без append / insert / pop у него.
    - append за O(1) амортизированно (удвоение ёмкости);
    - __getitem__ / __setitem__ за O(1), отрицательные индексы как у list, IndexError за границей;
    - pop() с конца за O(1), IndexError на пустом;
    - insert(i, x) за O(n); индекс за границей — вставка с краю, как у list;
    - __len__, __iter__.
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
