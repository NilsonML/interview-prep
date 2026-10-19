"""Паттерн 5. Бинарный поиск.     [неделя 3]

СИГНАЛЫ: массив отсортирован; «найти минимальное / максимальное X, при котором ...»;
ограничения до 10^9 (перебор невозможен); ответ монотонен: если скорость v подходит,
то и любая большая подходит.

ИДЕЯ: каждый шаг отбрасывает половину -> O(log n). Ищи не «элемент», а ГРАНИЦУ:
первую позицию, где условие становится истинным.
Аналогия: игра «угадай число от 1 до 1000» — хватает 10 вопросов.

ГЛАВНАЯ ЛОВУШКА — границы. Выбери один шаблон и всегда пиши его:
полуинтервал [lo, hi), while lo < hi, mid = (lo + hi) // 2,
условие истинно -> hi = mid, иначе lo = mid + 1. Ответ — lo.
"""

from math import ceil


def binary_search(nums: list[int], target: int) -> int:
    """LeetCode 704. Индекс target в отсортированном массиве или -1.

    >>> binary_search([-1, 0, 3, 5, 9, 12], 9)
    4
    """
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2  # в Python нет переполнения int, в Java/C++ пиши lo + (hi-lo)//2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def lower_bound(nums: list[int], target: int) -> int:
    """Первая позиция, куда можно вставить target, сохранив порядок (= bisect_left,
    LeetCode 35). Если target есть — индекс его первого вхождения.

    >>> lower_bound([1, 3, 3, 5], 3)
    1
    >>> lower_bound([1, 3, 5], 4)
    2

    Без модуля bisect.
    """
    lo, hi = 0, len(nums)  # ответ может быть len(nums) — поэтому hi не включается
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def search_rotated(nums: list[int], target: int) -> int:
    """LeetCode 33. Отсортированный массив без повторов сдвинут циклически
    ([4,5,6,7,0,1,2]). Индекс target или -1 за O(log n).

    >>> search_rotated([4, 5, 6, 7, 0, 1, 2], 0)
    4

    Подумай: после деления пополам одна из половин всегда отсортирована. Какая?
    """
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # левая половина отсортирована
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # правая половина отсортирована
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def find_min_rotated(nums: list[int]) -> int:
    """LeetCode 153. Минимум в циклически сдвинутом отсортированном массиве без повторов.

    >>> find_min_rotated([3, 4, 5, 1, 2])
    1
    """
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:  # минимум строго правее mid
            lo = mid + 1
        else:  # минимум в [lo, mid]
            hi = mid
    return nums[lo]


def min_eating_speed(piles: list[int], h: int) -> int:
    """LeetCode 875. Коко ест бананы: за час съедает до k бананов из ОДНОЙ кучки.
    Минимальное целое k, чтобы съесть всё за h часов (h >= len(piles)).

    >>> min_eating_speed([3, 6, 7, 11], 8)
    4

    Бинарный поиск ПО ОТВЕТУ: если скорость k успевает, то и k+1 успевает.
    """

    def hours(k: int) -> int:
        return sum(ceil(p / k) for p in piles)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours(mid) <= h:
            hi = mid  # mid подходит, но может есть меньше
        else:
            lo = mid + 1
    return lo


def int_sqrt(x: int) -> int:
    """LeetCode 69. Целая часть квадратного корня без math.sqrt и ** 0.5.

    >>> int_sqrt(8)
    2
    """
    lo, hi = 0, x + 1  # ищем первое m, у которого m*m > x; ответ на 1 меньше
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * mid > x:
            hi = mid
        else:
            lo = mid + 1
    return lo - 1
