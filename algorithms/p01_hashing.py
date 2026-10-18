"""Паттерн 1. Массивы и хеширование.

Главный вопрос паттерна: «что я ищу на каждом шаге и как найти это за O(1)?»
Почти всегда ответ — dict или set: обмениваем память O(n) на время O(1) на поиск.
"""


def contains_duplicate(nums: list[int]) -> bool:
    """LeetCode 217. Есть ли в массиве повторяющийся элемент.

    >>> contains_duplicate([1, 2, 3, 1])
    True
    >>> contains_duplicate([1, 2, 3])
    False

    Цель: O(n) времени.
    Подумай: какая структура мгновенно отвечает «видел ли я это раньше»?
    """
    raise NotImplementedError


def is_anagram(s: str, t: str) -> bool:
    """LeetCode 242. Является ли t анаграммой s (те же буквы в том же количестве).

    >>> is_anagram("listen", "silent")
    True
    >>> is_anagram("rat", "car")
    False

    Цель: O(n). Сортировка даёт O(n log n) — можно лучше.
    """
    raise NotImplementedError


def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    """LeetCode 1. Индексы i < j, для которых nums[i] + nums[j] == target.
    Решение гарантированно существует и единственно.

    >>> two_sum([2, 7, 11, 15], 9)
    (0, 1)

    Цель: O(n) за один проход.
    Подумай: для числа x ты ищешь target - x. Где его быстро найти?
    """
    raise NotImplementedError


def group_anagrams(words: list[str]) -> list[list[str]]:
    """LeetCode 49. Сгруппировать анаграммы.
    Порядок групп и слов внутри группы — по первому появлению во входе.

    >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

    Цель: O(n * k log k), k — длина слова.
    Подумай: каким должен быть КЛЮЧ словаря, чтобы все анаграммы к нему сошлись?
    """
    raise NotImplementedError


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """LeetCode 347. k самых частых элементов, от самого частого к менее частому.
    При равной частоте — меньшее число раньше.

    >>> top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    [1, 2]

    Цель: лучше, чем O(n log n). Подумай про bucket sort: частота не больше n.
    """
    raise NotImplementedError


def product_except_self(nums: list[int]) -> list[int]:
    """LeetCode 238. answer[i] = произведение всех элементов, кроме nums[i]. Делить нельзя.

    >>> product_except_self([1, 2, 3, 4])
    [24, 12, 8, 6]

    Цель: O(n) времени, O(1) доп. памяти не считая ответа.
    Подумай: произведение = (всё слева) * (всё справа).
    """
    raise NotImplementedError


def longest_consecutive(nums: list[int]) -> int:
    """LeetCode 128. Длина самой длинной последовательности подряд идущих чисел.

    >>> longest_consecutive([100, 4, 200, 1, 3, 2])
    4

    Цель: O(n) — сортировка не подходит.
    Подумай: с какого числа имеет смысл начинать отсчёт последовательности?
    """
    raise NotImplementedError
