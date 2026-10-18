"""Тесты паттернов 1–5: хеширование, два указателя, окно, стек, бинарный поиск.

Где возможно, кроме примеров есть стресс-тест: сверка с наивным решением на случайных
входах. Это главный способ найти ошибку в границах, когда примеры проходят.
"""

import bisect
import math
import random
from collections import Counter
from itertools import combinations

import pytest

from algorithms import (
    p01_hashing as h,
)
from algorithms import (
    p02_two_pointers as tp,
)
from algorithms import (
    p03_sliding_window as sw,
)
from algorithms import (
    p04_stack as st,
)
from algorithms import (
    p05_binary_search as bs,
)

rng = random.Random(42)

# ---------------------------------------------------------------- p01 hashing


def test_contains_duplicate():
    assert h.contains_duplicate([1, 2, 3, 1])
    assert not h.contains_duplicate([1, 2, 3])
    assert not h.contains_duplicate([])


def test_is_anagram():
    assert h.is_anagram("listen", "silent")
    assert not h.is_anagram("rat", "car")
    assert not h.is_anagram("aa", "a")


def test_two_sum():
    assert h.two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert h.two_sum([3, 3], 6) == (0, 1)
    assert h.two_sum([3, 2, 4], 6) == (1, 2)


def test_group_anagrams():
    assert h.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]) == [
        ["eat", "tea", "ate"],
        ["tan", "nat"],
        ["bat"],
    ]
    assert h.group_anagrams([""]) == [[""]]


def test_top_k_frequent():
    assert h.top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
    assert h.top_k_frequent([4, 4, 1, 1, 2], 2) == [1, 4]  # равная частота -> меньшее раньше
    for _ in range(50):
        nums = [rng.randint(0, 9) for _ in range(rng.randint(1, 40))]
        k = rng.randint(1, len(set(nums)))
        expected = [x for x, _ in sorted(Counter(nums).items(), key=lambda p: (-p[1], p[0]))][:k]
        assert h.top_k_frequent(nums, k) == expected


def test_product_except_self():
    assert h.product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert h.product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]


def test_longest_consecutive():
    assert h.longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert h.longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert h.longest_consecutive([]) == 0


# ---------------------------------------------------------------- p02 two pointers


def test_is_palindrome():
    assert tp.is_palindrome("A man, a plan, a canal: Panama")
    assert not tp.is_palindrome("race a car")
    assert tp.is_palindrome(" ")


def test_two_sum_sorted():
    assert tp.two_sum_sorted([2, 7, 11, 15], 9) == (0, 1)
    assert tp.two_sum_sorted([-1, 0], -1) == (0, 1)


def test_three_sum():
    assert tp.three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
    assert tp.three_sum([0, 0, 0, 0]) == [[0, 0, 0]]
    assert tp.three_sum([0, 1, 1]) == []
    for _ in range(50):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(0, 12))]
        expected = sorted({tuple(sorted(c)) for c in combinations(nums, 3) if sum(c) == 0})
        assert tp.three_sum(nums) == [list(t) for t in expected]


def test_max_area():
    assert tp.max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert tp.max_area([1, 1]) == 1


def test_remove_duplicates():
    a = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k = tp.remove_duplicates(a)
    assert k == 5 and a[:k] == [0, 1, 2, 3, 4]
    assert tp.remove_duplicates([]) == 0


def test_merge_sorted():
    assert tp.merge_sorted([1, 3, 5], [2, 4]) == [1, 2, 3, 4, 5]
    assert tp.merge_sorted([], [1]) == [1]
    for _ in range(50):
        a = sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 10)))
        b = sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 10)))
        assert tp.merge_sorted(a, b) == sorted(a + b)


# ---------------------------------------------------------------- p03 sliding window


def test_max_sum_window():
    assert sw.max_sum_window([2, 1, 5, 1, 3, 2], 3) == 9
    assert sw.max_sum_window([-1, -2, -3], 1) == -1


def test_max_profit():
    assert sw.max_profit([7, 1, 5, 3, 6, 4]) == 5
    assert sw.max_profit([7, 6, 4, 3, 1]) == 0
    for _ in range(100):
        p = [rng.randint(0, 50) for _ in range(rng.randint(1, 15))]
        brute = max([p[j] - p[i] for i in range(len(p)) for j in range(i + 1, len(p))] + [0])
        assert sw.max_profit(p) == brute


def test_length_of_longest_substring():
    assert sw.length_of_longest_substring("abcabcbb") == 3
    assert sw.length_of_longest_substring("bbbbb") == 1
    assert sw.length_of_longest_substring("pwwkew") == 3
    assert sw.length_of_longest_substring("abba") == 2  # ловушка: левая граница не идёт назад
    assert sw.length_of_longest_substring("") == 0
    for _ in range(100):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 12)))
        brute = max(
            [
                j - i
                for i in range(len(s))
                for j in range(i + 1, len(s) + 1)
                if len(set(s[i:j])) == j - i
            ]
            + [0]
        )
        assert sw.length_of_longest_substring(s) == brute


def test_character_replacement():
    assert sw.character_replacement("ABAB", 2) == 4
    assert sw.character_replacement("AABABBA", 1) == 4


def test_min_window():
    assert sw.min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert sw.min_window("a", "a") == "a"
    assert sw.min_window("a", "aa") == ""
    assert sw.min_window("aa", "aa") == "aa"


# ---------------------------------------------------------------- p04 stack


@pytest.mark.parametrize(
    "s, ok",
    [
        ("()", True),
        ("()[]{}", True),
        ("([]{})", True),
        ("", True),
        ("(]", False),
        ("((", False),
        (")(", False),
    ],
)
def test_is_valid_brackets(s, ok):
    assert st.is_valid_brackets(s) is ok


def test_eval_rpn():
    assert st.eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert st.eval_rpn(["4", "13", "5", "/", "+"]) == 6
    assert st.eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
    assert st.eval_rpn(["-7", "2", "/"]) == -3  # округление к нулю, а не вниз


def test_daily_temperatures():
    assert st.daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert st.daily_temperatures([30, 60, 90]) == [1, 1, 0]


def test_decode_string():
    assert st.decode_string("3[a]2[bc]") == "aaabcbc"
    assert st.decode_string("3[a2[c]]") == "accaccacc"
    assert st.decode_string("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert st.decode_string("10[a]") == "a" * 10


def test_largest_rectangle_area():
    assert st.largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
    assert st.largest_rectangle_area([2, 4]) == 4
    for _ in range(100):
        hs = [rng.randint(0, 6) for _ in range(rng.randint(1, 10))]
        brute = max(
            min(hs[i : j + 1]) * (j - i + 1) for i in range(len(hs)) for j in range(i, len(hs))
        )
        assert st.largest_rectangle_area(hs) == brute


# ---------------------------------------------------------------- p05 binary search


def test_binary_search():
    assert bs.binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert bs.binary_search([-1, 0, 3, 5, 9, 12], 2) == -1
    assert bs.binary_search([], 1) == -1
    for _ in range(200):
        nums = sorted(set(rng.randint(-20, 20) for _ in range(rng.randint(0, 15))))
        t = rng.randint(-22, 22)
        assert bs.binary_search(nums, t) == (nums.index(t) if t in nums else -1)


def test_lower_bound():
    for _ in range(300):
        nums = sorted(rng.randint(0, 10) for _ in range(rng.randint(0, 12)))
        t = rng.randint(-1, 11)
        assert bs.lower_bound(nums, t) == bisect.bisect_left(nums, t)


def test_search_rotated_and_min():
    assert bs.search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert bs.search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert bs.find_min_rotated([3, 4, 5, 1, 2]) == 1
    for _ in range(200):
        base = sorted(set(rng.randint(0, 50) for _ in range(rng.randint(1, 12))))
        k = rng.randrange(len(base))
        rotated = base[k:] + base[:k]
        t = rng.randint(-1, 51)
        assert bs.search_rotated(rotated, t) == (rotated.index(t) if t in rotated else -1)
        assert bs.find_min_rotated(rotated) == base[0]


def test_min_eating_speed():
    assert bs.min_eating_speed([3, 6, 7, 11], 8) == 4
    assert bs.min_eating_speed([30, 11, 23, 4, 20], 5) == 30
    assert bs.min_eating_speed([30, 11, 23, 4, 20], 6) == 23


def test_int_sqrt():
    for x in list(range(200)) + [2**31 - 1, 10**12]:
        assert bs.int_sqrt(x) == math.isqrt(x)
