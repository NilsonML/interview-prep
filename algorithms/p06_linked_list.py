"""Паттерн 6. Связные списки.     [неделя 4]

СИГНАЛЫ: дан ListNode; «на месте», «за один проход», «O(1) памяти».

ПРИЁМЫ:
    - dummy (сторожевой узел перед головой): убирает особый случай «изменилась голова»;
    - быстрый и медленный указатели: быстрый ходит через узел. Когда он дошёл до конца,
      медленный — в середине; если есть цикл, быстрый догонит медленного (как бегуны
      на круговом стадионе);
    - указатели с отставанием на n: n-й с конца за один проход;
    - разворот тремя указателями prev / current / next.
Совет: рисуй стрелки на бумаге. Ошибки в списках — это почти всегда потерянная ссылка.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def from_list(values: list[int]) -> ListNode | None:
    """Вспомогательная: [1, 2, 3] -> 1 -> 2 -> 3. Уже реализована."""
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head: ListNode | None) -> list[int]:
    """Вспомогательная: 1 -> 2 -> 3 -> [1, 2, 3]. Уже реализована."""
    result = []
    while head is not None:
        result.append(head.val)
        head = head.next
    return result


def reverse_list(head: ListNode | None) -> ListNode | None:
    """LeetCode 206. Развернуть список, вернуть новую голову. O(n) времени, O(1) памяти.

    >>> to_list(reverse_list(from_list([1, 2, 3])))
    [3, 2, 1]
    """
    prev = None
    while head is not None:
        head.next, prev, head = prev, head, head.next
    return prev


def merge_two_lists(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    """LeetCode 21. Слить два отсортированных списка, переиспользуя узлы.

    >>> to_list(merge_two_lists(from_list([1, 2, 4]), from_list([1, 3, 4])))
    [1, 1, 2, 3, 4, 4]
    """
    dummy = tail = ListNode(0)  # сторож: не нужно отдельно выбирать голову результата
    while a is not None and b is not None:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


def has_cycle(head: ListNode | None) -> bool:
    """LeetCode 141. Есть ли в списке цикл. O(1) памяти (без set посещённых).

    Подумай: алгоритм Флойда «черепаха и заяц». Если цикл есть, быстрый догонит медленного.
    """
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False


def middle_node(head: ListNode | None) -> ListNode | None:
    """LeetCode 876. Средний узел; при чётной длине — второй из двух средних.

    >>> to_list(middle_node(from_list([1, 2, 3, 4, 5])))
    [3, 4, 5]
    """
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
    return slow


def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    """LeetCode 19. Удалить n-й узел с конца за один проход (1 <= n <= длина).

    >>> to_list(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2))
    [1, 2, 3, 5]

    Подумай: два указателя на расстоянии n. Зачем здесь dummy?
    """
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):  # fast уходит на n+1 вперёд, чтобы slow встал ПЕРЕД удаляемым
        fast = fast.next
    while fast is not None:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
    return dummy.next  # голова могла удалиться — поэтому не head
