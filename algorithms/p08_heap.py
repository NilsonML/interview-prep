"""Паттерн 8. Куча (heapq).     [неделя 6]

СИГНАЛЫ: «k наибольших / наименьших / ближайших», «k-й по величине», «слить k
отсортированных», «медиана потока», «каждый раз брать минимум / максимум».

ИДЕЯ: куча за O(log n) отдаёт минимум и принимает новый элемент. Куча РАЗМЕРА k
держит k лучших: O(n log k) вместо сортировки O(n log n).
Аналогия: доска почёта на k мест — новый кандидат вытесняет самого слабого из k.

PYTHON: heapq — только min-heap. Max-heap: кладём -x. Кортежи сравниваются
поэлементно: (приоритет, номер, объект) — номер разрешает ничьи.
"""

import heapq


def kth_largest(nums: list[int], k: int) -> int:
    """LeetCode 215. k-й по величине элемент (с учётом повторов).

    >>> kth_largest([3, 2, 1, 5, 6, 4], 2)
    5

    Цель: O(n log k). Подумай: min-heap из k элементов — что лежит на её вершине?
    """
    heap: list[int] = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)  # выкидываем меньший: в куче остаются k наибольших
    return heap[0]


def k_closest(points: list[tuple[int, int]], k: int) -> list[tuple[int, int]]:
    """LeetCode 973. k ближайших к началу координат точек, отсортированных по расстоянию
    (при равенстве — по самой точке).

    >>> k_closest([(1, 3), (-2, 2)], 1)
    [(-2, 2)]
    """
    # nsmallest сам держит кучу размера k. Ключ без sqrt: монотонность сохраняется.
    return heapq.nsmallest(k, points, key=lambda p: (p[0] ** 2 + p[1] ** 2, p))


def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    """LeetCode 23 (на массивах). Слить k отсортированных списков.

    >>> merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]])
    [1, 1, 2, 3, 4, 4, 5, 6]

    Цель: O(N log k), N — всего элементов. Без sorted() по всем элементам.
    """
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]  # (значение, список, позиция)
    heapq.heapify(heap)
    result = []
    while heap:
        value, i, j = heapq.heappop(heap)
        result.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return result


def last_stone_weight(stones: list[int]) -> int:
    """LeetCode 1046. Каждый ход сталкиваем два самых тяжёлых камня x <= y:
    если равны — оба исчезают, иначе остаётся y - x. Вес последнего камня или 0.

    >>> last_stone_weight([2, 7, 4, 1, 8, 1])
    1
    """
    heap = [-s for s in stones]  # max-heap через отрицательные числа
    heapq.heapify(heap)
    while len(heap) > 1:
        y, x = -heapq.heappop(heap), -heapq.heappop(heap)
        if y != x:
            heapq.heappush(heap, -(y - x))
    return -heap[0] if heap else 0


class MedianFinder:
    """LeetCode 295 (hard). Медиана потока чисел.

    add_num(x) за O(log n), find_median() за O(1).

    Подумай: две кучи — max-heap для меньшей половины и min-heap для большей.
    Какой инвариант на их размеры нужно поддерживать?
    """

    def __init__(self) -> None:
        self._low: list[int] = []  # max-heap (отрицательные), меньшая половина
        self._high: list[int] = []  # min-heap, большая половина

    def add_num(self, num: int) -> None:
        heapq.heappush(self._low, -num)
        # Самый большой из меньшей половины переезжает в большую: порядок между кучами
        heapq.heappush(self._high, -heapq.heappop(self._low))
        if len(self._high) > len(self._low):  # инвариант: len(low) >= len(high)
            heapq.heappush(self._low, -heapq.heappop(self._high))

    def find_median(self) -> float:
        if len(self._low) > len(self._high):
            return float(-self._low[0])
        return (-self._low[0] + self._high[0]) / 2
