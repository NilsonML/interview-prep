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
        self.head: Node | None = None
        self.tail: Node | None = None
        self._size = 0

    def push_front(self, value: Any) -> None:
        self.head = Node(value, self.head)
        if self.tail is None:  # список был пуст: новый узел — и голова, и хвост
            self.tail = self.head
        self._size += 1

    def push_back(self, value: Any) -> None:
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def pop_front(self) -> Any:
        if self.head is None:
            raise IndexError("pop from empty list")
        node = self.head
        self.head = node.next
        if self.head is None:  # удалили последний узел
            self.tail = None
        self._size -= 1
        return node.value

    def find(self, value: Any) -> bool:
        node = self.head
        while node is not None:
            if node.value == value:
                return True
            node = node.next
        return False

    def reverse(self) -> None:
        # Три указателя: prev <- current, затем сдвигаемся. Каждую ссылку разворачиваем один раз.
        prev, current = None, self.head
        self.tail = self.head
        while current is not None:
            nxt = current.next
            current.next = prev
            prev, current = current, nxt
        self.head = prev

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next
