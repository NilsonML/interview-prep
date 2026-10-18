"""Стек и очередь.

Задание 1. MinStack: стек, который за O(1) отдаёт текущий минимум (LeetCode 155).
    push(x), pop() -> x, top() -> x, get_min() -> x; IndexError на пустом.
    Подумай: что нужно хранить, чтобы после pop() минимум "вспомнил" предыдущее значение?

Задание 2. QueueFromStacks: очередь (FIFO) на двух стеках (LeetCode 232).
    enqueue(x), dequeue() -> x, peek() -> x за O(1) амортизированно, IndexError на пустой,
    __len__. Можно использовать только list.append / list.pop() (с конца).
    Подумай: почему каждый элемент перекладывается не больше одного раза?

Задание 3. RingBuffer: очередь фиксированной ёмкости на массиве с "закольцованными" индексами.
    enqueue(x) -> OverflowError при переполнении, dequeue() -> x, IndexError на пустой, __len__.
    Так устроены буферы в сетевых драйверах и логах: память не выделяется после создания.
"""

from typing import Any


class MinStack:
    def __init__(self) -> None:
        raise NotImplementedError

    def push(self, value: Any) -> None:
        raise NotImplementedError

    def pop(self) -> Any:
        raise NotImplementedError

    def top(self) -> Any:
        raise NotImplementedError

    def get_min(self) -> Any:
        raise NotImplementedError


class QueueFromStacks:
    def __init__(self) -> None:
        raise NotImplementedError

    def enqueue(self, value: Any) -> None:
        raise NotImplementedError

    def dequeue(self) -> Any:
        raise NotImplementedError

    def peek(self) -> Any:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


class RingBuffer:
    def __init__(self, capacity: int) -> None:
        raise NotImplementedError

    def enqueue(self, value: Any) -> None:
        raise NotImplementedError

    def dequeue(self) -> Any:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
