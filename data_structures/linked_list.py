"""Односвязный список.     [обязательно · неделя 4]

ИНТУИЦИЯ
    Квест «найди записку»: в каждой записке — подарок (value) и где искать следующую (next).
    Вставить новую записку в начало — секунда. Найти десятую — пройти девять.

КАК УСТРОЕНО
    head -> [1 | •] -> [2 | •] -> [3 | None] <- tail

    push_front(0):  новый узел указывает на старый head, head = новый узел.        O(1)
    push_back(4):   tail.next = новый узел, tail = новый узел (поэтому храним tail). O(1)
    pop_front():    head = head.next.                                                O(1)
    reverse():      идём по списку и разворачиваем каждую стрелку:
                    None <- 1    2 -> 3        (prev, current, next — три указателя)
                    None <- 1 <- 2    3
                    None <- 1 <- 2 <- 3        head = 3, tail = 1

ТЕРМИНЫ
    узел (node), указатель (ссылка), голова и хвост, сторожевой узел (dummy / sentinel).

ТИПИЧНЫЕ ОШИБКИ
    - потерять ссылку на «следующий» до того, как переписал current.next;
    - удалить последний узел и забыть обнулить tail (или наоборот, head);
    - после reverse не обновить tail.

ЗАДАНИЕ
    - push_front / pop_front за O(1), IndexError при pop из пустого;
    - push_back за O(1) (храни tail);
    - find(value) -> bool за O(n);
    - reverse() на месте: O(n) времени, O(1) памяти;
    - __len__ за O(1), __iter__ по значениям.
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
