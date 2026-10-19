"""Модуль collections: Counter, defaultdict, deque.     [неделя 3]

На интервью ответ «я бы взял Counter» часто лучше десяти строк ручного подсчёта.
    Counter      — dict-счётчик: Counter(words).most_common(3); счётчики можно складывать;
    defaultdict  — dict со значением по умолчанию: defaultdict(list) для группировки;
    deque        — двусторонняя очередь: append / appendleft / pop / popleft за O(1)
                   (у list pop(0) — O(n)); deque(maxlen=k) — окно последних k элементов.
Монотонная очередь (последняя задача) — deque, где значения упорядочены; родственник
монотонного стека из паттерна 4.
"""

import re
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Hashable, Iterable
from typing import Any


def first_unique_char(s: str) -> int:
    """LeetCode 387. Индекс первого неповторяющегося символа или -1.

    >>> first_unique_char("leetcode")
    0
    >>> first_unique_char("aabb")
    -1
    """
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


def group_by(items: Iterable[Any], key: Callable[[Any], Hashable]) -> dict[Hashable, list[Any]]:
    """Сгруппировать элементы по ключу, сохраняя порядок (как GROUP BY в SQL).

    >>> group_by(["apple", "avocado", "banana"], key=lambda w: w[0])
    {'a': ['apple', 'avocado'], 'b': ['banana']}
    """
    groups: defaultdict[Hashable, list[Any]] = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    return dict(groups)


def merge_counts(*dicts: dict[str, int]) -> dict[str, int]:
    """Сложить счётчики из нескольких словарей.

    >>> merge_counts({"a": 1, "b": 2}, {"b": 3, "c": 1})
    {'a': 1, 'b': 5, 'c': 1}
    """
    total: Counter[str] = Counter()
    for d in dicts:
        total.update(d)  # update у Counter СКЛАДЫВАЕТ, а у dict — перезаписывает
    return dict(total)


def most_common_words(text: str, k: int) -> list[tuple[str, int]]:
    """k самых частых слов (нижний регистр, только буквы и цифры). При равенстве — по алфавиту.

    >>> most_common_words("b a, A! b c a", 2)
    [('a', 3), ('b', 2)]
    """
    counts = Counter(re.findall(r"\w+", text.lower()))
    return sorted(counts.items(), key=lambda p: (-p[1], p[0]))[:k]


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    """LeetCode 239 (hard). Максимум в каждом окне длины k.

    >>> sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
    [3, 3, 5, 5, 6, 7]

    Цель: O(n). Монотонная очередь (deque) индексов с убывающими значениями.
    """
    window: deque[int] = deque()
    result = []
    for i, x in enumerate(nums):
        while window and nums[window[-1]] <= x:
            window.pop()  # меньшие элементы уже никогда не станут максимумом
        window.append(i)
        if window[0] <= i - k:
            window.popleft()  # вышел за левую границу окна
        if i >= k - 1:
            result.append(nums[window[0]])
    return result
