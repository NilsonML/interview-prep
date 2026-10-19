"""Паттерн 1. Массивы и хеширование.     [неделя 1]

СИГНАЛЫ В УСЛОВИИ: «найти пару / дубликат», «сгруппировать», «посчитать частоты»,
«встречался ли раньше», а наивное решение — вложенный цикл O(n^2).

ИДЕЯ: на каждом шаге спроси «что я ищу?» и сделай так, чтобы найти это за O(1):
положи уже просмотренное в dict или set. Обмен памяти O(n) на время.
Аналогия: вместо того чтобы каждый раз обходить весь склад, заводишь картотеку.

ИНСТРУМЕНТЫ: set (было / не было), dict (значение -> индекс / счётчик), Counter,
defaultdict(list) (группировка), sorted(word) или кортеж частот как ключ.
"""

from collections import Counter, defaultdict


def contains_duplicate(nums: list[int]) -> bool:
    """LeetCode 217. Есть ли в массиве повторяющийся элемент.

    >>> contains_duplicate([1, 2, 3, 1])
    True
    >>> contains_duplicate([1, 2, 3])
    False

    Цель: O(n) времени.
    Подумай: какая структура мгновенно отвечает «видел ли я это раньше»?
    """
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


def is_anagram(s: str, t: str) -> bool:
    """LeetCode 242. Является ли t анаграммой s (те же буквы в том же количестве).

    >>> is_anagram("listen", "silent")
    True
    >>> is_anagram("rat", "car")
    False

    Цель: O(n). Сортировка даёт O(n log n) — можно лучше.
    """
    return len(s) == len(t) and Counter(s) == Counter(t)


def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    """LeetCode 1. Индексы i < j, для которых nums[i] + nums[j] == target.
    Решение гарантированно существует и единственно.

    >>> two_sum([2, 7, 11, 15], 9)
    (0, 1)

    Цель: O(n) за один проход.
    Подумай: для числа x ты ищешь target - x. Где его быстро найти?
    """
    seen: dict[int, int] = {}  # число -> индекс
    for j, x in enumerate(nums):
        if target - x in seen:
            return seen[target - x], j
        seen[x] = j  # после проверки: иначе [3, 3] с target 6 найдёт x в паре с собой
    raise ValueError("no solution")


def group_anagrams(words: list[str]) -> list[list[str]]:
    """LeetCode 49. Сгруппировать анаграммы.
    Порядок групп и слов внутри группы — по первому появлению во входе.

    >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

    Цель: O(n * k log k), k — длина слова.
    Подумай: каким должен быть КЛЮЧ словаря, чтобы все анаграммы к нему сошлись?
    """
    groups: dict[str, list[str]] = defaultdict(list)  # dict хранит порядок вставки
    for w in words:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """LeetCode 347. k самых частых элементов, от самого частого к менее частому.
    При равной частоте — меньшее число раньше.

    >>> top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    [1, 2]

    Цель: лучше, чем O(n log n). Подумай про bucket sort: частота не больше n.
    """
    counts = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]  # индекс = частота
    for x, c in counts.items():
        buckets[c].append(x)
    result: list[int] = []
    for c in range(len(buckets) - 1, 0, -1):
        for x in sorted(buckets[c]):
            result.append(x)
            if len(result) == k:
                return result
    return result


def product_except_self(nums: list[int]) -> list[int]:
    """LeetCode 238. answer[i] = произведение всех элементов, кроме nums[i]. Делить нельзя.

    >>> product_except_self([1, 2, 3, 4])
    [24, 12, 8, 6]

    Цель: O(n) времени, O(1) доп. памяти не считая ответа.
    Подумай: произведение = (всё слева) * (всё справа).
    """
    n = len(nums)
    answer = [1] * n
    left = 1
    for i in range(n):  # проход слева: answer[i] = произведение левее i
        answer[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):  # проход справа: домножаем на произведение правее i
        answer[i] *= right
        right *= nums[i]
    return answer


def longest_consecutive(nums: list[int]) -> int:
    """LeetCode 128. Длина самой длинной последовательности подряд идущих чисел.

    >>> longest_consecutive([100, 4, 200, 1, 3, 2])
    4

    Цель: O(n) — сортировка не подходит.
    Подумай: с какого числа имеет смысл начинать отсчёт последовательности?
    """
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 not in values:  # x — начало последовательности, считаем только отсюда
            length = 1
            while x + length in values:
                length += 1
            best = max(best, length)
    return best  # каждое число просматривается O(1) раз -> O(n)
