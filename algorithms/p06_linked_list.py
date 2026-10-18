"""Паттерн 6. Связные списки.

Приёмы: фиктивный узел (dummy) перед головой — убирает особый случай «изменилась голова»;
быстрый и медленный указатели — середина списка, поиск цикла, n-й с конца.
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
    raise NotImplementedError


def merge_two_lists(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    """LeetCode 21. Слить два отсортированных списка, переиспользуя узлы.

    >>> to_list(merge_two_lists(from_list([1, 2, 4]), from_list([1, 3, 4])))
    [1, 1, 2, 3, 4, 4]
    """
    raise NotImplementedError


def has_cycle(head: ListNode | None) -> bool:
    """LeetCode 141. Есть ли в списке цикл. O(1) памяти (без set посещённых).

    Подумай: алгоритм Флойда «черепаха и заяц». Если цикл есть, быстрый догонит медленного.
    """
    raise NotImplementedError


def middle_node(head: ListNode | None) -> ListNode | None:
    """LeetCode 876. Средний узел; при чётной длине — второй из двух средних.

    >>> to_list(middle_node(from_list([1, 2, 3, 4, 5])))
    [3, 4, 5]
    """
    raise NotImplementedError


def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    """LeetCode 19. Удалить n-й узел с конца за один проход (1 <= n <= длина).

    >>> to_list(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2))
    [1, 2, 3, 5]

    Подумай: два указателя на расстоянии n. Зачем здесь dummy?
    """
    raise NotImplementedError
