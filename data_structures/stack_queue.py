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
        # Храним пары (значение, минимум на момент вставки):
        # после pop минимум автоматически "откатывается".
        self._items: list[tuple[Any, Any]] = []

    def push(self, value: Any) -> None:
        current_min = value if not self._items else min(value, self._items[-1][1])
        self._items.append((value, current_min))

    def pop(self) -> Any:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()[0]

    def top(self) -> Any:
        if not self._items:
            raise IndexError("top from empty stack")
        return self._items[-1][0]

    def get_min(self) -> Any:
        if not self._items:
            raise IndexError("min from empty stack")
        return self._items[-1][1]


class QueueFromStacks:
    def __init__(self) -> None:
        self._in: list[Any] = []  # сюда кладём
        self._out: list[Any] = []  # отсюда забираем (в обратном порядке)

    def _shift(self) -> None:
        # Перекладываем, только когда _out пуст: каждый элемент переезжает ровно один раз
        # -> суммарно O(n) на n операций -> O(1) амортизированно.
        if not self._out:
            while self._in:
                self._out.append(self._in.pop())

    def enqueue(self, value: Any) -> None:
        self._in.append(value)

    def dequeue(self) -> Any:
        self._shift()
        if not self._out:
            raise IndexError("dequeue from empty queue")
        return self._out.pop()

    def peek(self) -> Any:
        self._shift()
        if not self._out:
            raise IndexError("peek from empty queue")
        return self._out[-1]

    def __len__(self) -> int:
        return len(self._in) + len(self._out)


class RingBuffer:
    def __init__(self, capacity: int) -> None:
        self._data: list[Any] = [None] * capacity
        self._head = 0  # индекс первого элемента
        self._size = 0

    def enqueue(self, value: Any) -> None:
        if self._size == len(self._data):
            raise OverflowError("buffer is full")
        tail = (self._head + self._size) % len(self._data)  # % "заворачивает" индекс в начало
        self._data[tail] = value
        self._size += 1

    def dequeue(self) -> Any:
        if self._size == 0:
            raise IndexError("dequeue from empty buffer")
        value = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % len(self._data)
        self._size -= 1
        return value

    def __len__(self) -> int:
        return self._size
