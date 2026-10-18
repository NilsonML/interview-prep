"""Бинарная куча (min-heap) на массиве.

Задание: реализуй кучу без модуля heapq.

Требования:
    - push за O(log n): кладём в конец и "всплываем" (sift up);
    - pop() -> минимум за O(log n): последний элемент в корень и "тонем" (sift down);
      IndexError на пустой;
    - peek() -> минимум за O(1);
    - heapify(items) -> MinHeap за O(n) (а не O(n log n) через n push!);
    - __len__.

Устройство: дети узла i — 2i+1 и 2i+2, родитель — (i-1)//2.

Подумай до кода:
    - Почему heapify за O(n)? Подсказка: большинство узлов — внизу, и тонуть им недалеко.
    - Где куча нужна в задачах? (top-k, слияние k списков, Дейкстра, медиана потока)
"""

from typing import Any


class MinHeap:
    def __init__(self) -> None:
        raise NotImplementedError

    @classmethod
    def heapify(cls, items: list[Any]) -> "MinHeap":
        raise NotImplementedError

    def push(self, value: Any) -> None:
        raise NotImplementedError

    def pop(self) -> Any:
        raise NotImplementedError

    def peek(self) -> Any:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
