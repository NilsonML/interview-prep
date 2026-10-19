"""Стек и очередь: три задачи с интервью.     [обязательно · неделя 3]

ИНТУИЦИЯ
    Стек — стопка тарелок: кладёшь и берёшь сверху (LIFO, last in — first out).
    Очередь — очередь в кассу: пришёл первым — обслужен первым (FIFO).

1. MinStack (LeetCode 155): стек, который за O(1) знает текущий минимум.
    Идея: вместе с каждым значением храни «минимум на момент вставки».
        push 5  -> [(5, 5)]
        push 3  -> [(5, 5), (3, 3)]
        push 7  -> [(5, 5), (3, 3), (7, 3)]    минимум 3
        pop     -> [(5, 5), (3, 3)]            минимум снова 3 — «вспоминается» сам
    Методы: push(x), pop() -> x, top() -> x, get_min() -> x; IndexError на пустом.

2. QueueFromStacks (LeetCode 232): очередь на двух стеках.
    in_stack — куда кладём, out_stack — откуда берём. Когда out пуст, перекладываем
    в него всё из in: порядок переворачивается и становится FIFO.
        enqueue 1, 2, 3   in = [1, 2, 3]   out = []
        dequeue           in = []          out = [3, 2, 1] -> pop() -> 1
    Каждый элемент перекладывается ровно один раз -> O(1) амортизированно.
    Методы: enqueue(x), dequeue() -> x, peek() -> x, __len__; IndexError на пустой.
    Можно использовать только list.append и list.pop() с конца.

3. RingBuffer: очередь фиксированной ёмкости на массиве, индексы «закольцованы».
    capacity = 4, head = 2, size = 3:   [ c, _, a, b ]    очередь: a, b, c
    следующий свободный = (head + size) % capacity = 1
    Так устроены буферы логов и сетевые очереди: память выделяется один раз.
    Методы: enqueue(x) (OverflowError при переполнении), dequeue() -> x
    (IndexError на пустой), __len__.

ТЕРМИНЫ: LIFO, FIFO, амортизированная сложность, кольцевой буфер, deque.
В задачах бери collections.deque — это и стек, и очередь с O(1) на обоих концах.
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
