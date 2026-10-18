"""Модуль collections и встроенные структуры: Counter, defaultdict, deque.

Знать стандартную библиотеку — это тоже навык с интервью: ответ «я бы взял Counter»
часто лучше десяти строк ручного подсчёта.
"""

from collections.abc import Callable, Hashable, Iterable
from typing import Any


def first_unique_char(s: str) -> int:
    """LeetCode 387. Индекс первого неповторяющегося символа или -1.

    >>> first_unique_char("leetcode")
    0
    >>> first_unique_char("aabb")
    -1
    """
    raise NotImplementedError


def group_by(items: Iterable[Any], key: Callable[[Any], Hashable]) -> dict[Hashable, list[Any]]:
    """Сгруппировать элементы по ключу, сохраняя порядок (как GROUP BY в SQL).

    >>> group_by(["apple", "avocado", "banana"], key=lambda w: w[0])
    {'a': ['apple', 'avocado'], 'b': ['banana']}
    """
    raise NotImplementedError


def merge_counts(*dicts: dict[str, int]) -> dict[str, int]:
    """Сложить счётчики из нескольких словарей.

    >>> merge_counts({"a": 1, "b": 2}, {"b": 3, "c": 1})
    {'a': 1, 'b': 5, 'c': 1}
    """
    raise NotImplementedError


def most_common_words(text: str, k: int) -> list[tuple[str, int]]:
    """k самых частых слов (нижний регистр, только буквы и цифры). При равенстве — по алфавиту.

    >>> most_common_words("b a, A! b c a", 2)
    [('a', 3), ('b', 2)]
    """
    raise NotImplementedError


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    """LeetCode 239 (hard). Максимум в каждом окне длины k.

    >>> sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
    [3, 3, 5, 5, 6, 7]

    Цель: O(n). Монотонная очередь (deque) индексов с убывающими значениями.
    """
    raise NotImplementedError
