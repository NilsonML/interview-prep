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
        self._data: list[Any] = [None] * capacity
        self._size = 0

    @property
    def capacity(self) -> int:
        return len(self._data)

    def _normalize(self, index: int) -> int:
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("index out of range")
        return index

    def _grow(self) -> None:
        # Удвоение: дорогое копирование O(n) происходит всё реже, суммарно n append
        # стоят O(n). При росте на константу +k было бы O(n^2 / k).
        new_data = [None] * (2 * len(self._data) or 1)
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data

    def append(self, value: Any) -> None:
        if self._size == len(self._data):
            self._grow()
        self._data[self._size] = value
        self._size += 1

    def insert(self, index: int, value: Any) -> None:
        index = max(0, min(index, self._size))  # как list.insert: за границей вставляем с краю
        if self._size == len(self._data):
            self._grow()
        for i in range(self._size, index, -1):  # сдвиг вправо, идём с конца
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def pop(self) -> Any:
        if self._size == 0:
            raise IndexError("pop from empty array")
        self._size -= 1
        value = self._data[self._size]
        self._data[self._size] = None  # не держим ссылку: объект сможет удалиться из памяти
        return value

    def __getitem__(self, index: int) -> Any:
        return self._data[self._normalize(index)]

    def __setitem__(self, index: int, value: Any) -> None:
        self._data[self._normalize(index)] = value

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        for i in range(self._size):
            yield self._data[i]
