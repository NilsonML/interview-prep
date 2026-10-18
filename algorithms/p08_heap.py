"""Паттерн 8. Куча (приоритетная очередь), модуль heapq.

Когда применять: «k наибольших / наименьших», «k ближайших», слияние k отсортированных
потоков, медиана потока. Куча размера k даёт O(n log k) вместо сортировки O(n log n).
heapq в Python — только min-heap; для max-heap кладут -x.
"""


def kth_largest(nums: list[int], k: int) -> int:
    """LeetCode 215. k-й по величине элемент (с учётом повторов).

    >>> kth_largest([3, 2, 1, 5, 6, 4], 2)
    5

    Цель: O(n log k). Подумай: min-heap из k элементов — что лежит на её вершине?
    """
    raise NotImplementedError


def k_closest(points: list[tuple[int, int]], k: int) -> list[tuple[int, int]]:
    """LeetCode 973. k ближайших к началу координат точек, отсортированных по расстоянию
    (при равенстве — по самой точке).

    >>> k_closest([(1, 3), (-2, 2)], 1)
    [(-2, 2)]
    """
    raise NotImplementedError


def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    """LeetCode 23 (на массивах). Слить k отсортированных списков.

    >>> merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]])
    [1, 1, 2, 3, 4, 4, 5, 6]

    Цель: O(N log k), N — всего элементов. Без sorted() по всем элементам.
    """
    raise NotImplementedError


def last_stone_weight(stones: list[int]) -> int:
    """LeetCode 1046. Каждый ход сталкиваем два самых тяжёлых камня x <= y:
    если равны — оба исчезают, иначе остаётся y - x. Вес последнего камня или 0.

    >>> last_stone_weight([2, 7, 4, 1, 8, 1])
    1
    """
    raise NotImplementedError


class MedianFinder:
    """LeetCode 295 (hard). Медиана потока чисел.

    add_num(x) за O(log n), find_median() за O(1).

    Подумай: две кучи — max-heap для меньшей половины и min-heap для большей.
    Какой инвариант на их размеры нужно поддерживать?
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def add_num(self, num: int) -> None:
        raise NotImplementedError

    def find_median(self) -> float:
        raise NotImplementedError
