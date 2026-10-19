"""Паттерн 3. Скользящее окно.     [неделя 2]

СИГНАЛЫ: «самая длинная / короткая ПОДСТРОКА или ПОДМАССИВ (подряд идущие)»,
«не более k ...», «содержит все символы ...», «сумма окна длины k».

ИДЕЯ: окно [left, right] растёт справа; когда условие нарушено — сжимается слева.
Каждый элемент входит в окно и выходит из него по разу -> O(n).
Аналогия: гусеница — передний конец ползёт вперёд, задний подтягивается.

ДВА ВИДА: фиксированной длины (сдвигаем и пересчитываем сумму за O(1)) и
переменной (растём, пока можно; сжимаемся, пока нельзя). Состояние окна держи в
счётчике (Counter / dict), а не пересчитывай с нуля.
"""

from collections import Counter


def max_sum_window(nums: list[int], k: int) -> int:
    """Максимальная сумма подмассива длины ровно k (окно фиксированного размера).

    >>> max_sum_window([2, 1, 5, 1, 3, 2], 3)
    9

    Цель: O(n), а не O(n*k). Подумай: как пересчитать сумму при сдвиге окна на 1?
    """
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]  # вошёл справа, вышел слева
        best = max(best, window)
    return best


def max_profit(prices: list[int]) -> int:
    """LeetCode 121. Купить в один день, продать в более поздний. Максимальная прибыль
    (0, если заработать нельзя).

    >>> max_profit([7, 1, 5, 3, 6, 4])
    5

    Цель: O(n), один проход.
    """
    min_price = float("inf")
    best = 0
    for p in prices:
        min_price = min(min_price, p)  # лучший день покупки среди прошедших
        best = max(best, p - min_price)
    return best


def length_of_longest_substring(s: str) -> int:
    """LeetCode 3. Длина самой длинной подстроки без повторяющихся символов.

    >>> length_of_longest_substring("abcabcbb")
    3

    Цель: O(n). Подумай: что делать с левой границей, когда встретили повтор?
    """
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(s):
        if last_seen.get(ch, -1) >= left:
            left = last_seen[ch] + 1  # прыгаем сразу за предыдущее вхождение
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


def character_replacement(s: str, k: int) -> int:
    """LeetCode 424. Можно заменить не более k символов. Длина самой длинной подстроки
    из одинаковых символов, которую можно получить.

    >>> character_replacement("AABABBA", 1)
    4

    Цель: O(n). Подумай: окно валидно, если (длина окна - частота самого частого) <= k.
    """
    counts: Counter[str] = Counter()
    left = max_freq = best = 0
    for right, ch in enumerate(s):
        counts[ch] += 1
        max_freq = max(max_freq, counts[ch])
        while (right - left + 1) - max_freq > k:
            counts[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def min_window(s: str, t: str) -> str:
    """LeetCode 76 (hard). Самая короткая подстрока s, содержащая все символы t
    (с учётом кратности). Если нет — "". Если таких несколько — самая левая.

    >>> min_window("ADOBECODEBANC", "ABC")
    'BANC'

    Цель: O(len(s) + len(t)).
    Подумай: расширяй окно, пока не покрыло t; потом сжимай слева, пока покрывает.
    """
    if not t:
        return ""
    need = Counter(t)
    missing = len(t)  # сколько символов t ещё не покрыто
    left = 0
    best_start, best_len = 0, float("inf")
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left + 1 < best_len:
                best_start, best_len = left, right - left + 1
            need[s[left]] += 1
            if need[s[left]] > 0:  # убрали нужный символ — окно перестало покрывать t
                missing += 1
            left += 1
    return "" if best_len == float("inf") else s[best_start : best_start + best_len]
