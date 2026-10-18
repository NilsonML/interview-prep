"""Односвязный список.

Задание: реализуй список из узлов Node(value, next).

Требования:
    - push_front / pop_front за O(1);
    - push_back за O(1): храни ссылку на хвост (tail);
    - find(value) -> bool за O(n);
    - reverse() на месте за O(n) времени и O(1) памяти — классика интервью;
    - __len__ за O(1), __iter__ по значениям.

Подумай до кода:
    - Какие операции у связного списка быстрее, чем у массива, а какие медленнее?
    - Что нужно обновить, когда удаляется последний оставшийся узел?
"""

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    value: Any
    next: Optional["Node"] = None


class LinkedList:
    def __init__(self) -> None:
        raise NotImplementedError

    def push_front(self, value: Any) -> None:
        raise NotImplementedError

    def push_back(self, value: Any) -> None:
        raise NotImplementedError

    def pop_front(self) -> Any:
        raise NotImplementedError

    def find(self, value: Any) -> bool:
        raise NotImplementedError

    def reverse(self) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[Any]:
        raise NotImplementedError
