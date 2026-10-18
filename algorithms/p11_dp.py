"""Паттерн 11. Динамическое программирование.

Когда применять: оптимизация (минимум / максимум / число способов), и решение большой
задачи складывается из решений перекрывающихся меньших. Рецепт:
    1. Состояние: что означает dp[i] (или dp[i][j])? Сформулируй словами.
    2. Переход: как dp[i] выражается через меньшие состояния?
    3. База: значения для самых маленьких состояний.
    4. Порядок вычисления и где ответ.
Начинай с рекурсии + @cache (сверху вниз), потом переписывай в таблицу (снизу вверх).
"""


def climb_stairs(n: int) -> int:
    """LeetCode 70. Число способов подняться на n ступенек шагами по 1 или 2.

    >>> climb_stairs(3)
    3

    dp[i] = dp[i-1] + dp[i-2]. Цель: O(n) времени, O(1) памяти.
    """
    raise NotImplementedError


def rob(houses: list[int]) -> int:
    """LeetCode 198. Максимальная сумма без двух соседних домов.

    >>> rob([2, 7, 9, 3, 1])
    12
    """
    raise NotImplementedError


def coin_change(coins: list[int], amount: int) -> int:
    """LeetCode 322. Минимальное число монет на сумму amount (монет каждого номинала
    сколько угодно); -1, если нельзя.

    >>> coin_change([1, 2, 5], 11)
    3

    Подумай: почему жадный алгоритм «берём самую крупную» ошибается на [1, 3, 4], 6?
    """
    raise NotImplementedError


def length_of_lis(nums: list[int]) -> int:
    """LeetCode 300. Длина наибольшей строго возрастающей подпоследовательности.

    >>> length_of_lis([10, 9, 2, 5, 3, 7, 101, 18])
    4

    Сначала O(n^2): dp[i] — длина LIS, заканчивающейся в i. Бонус: O(n log n).
    """
    raise NotImplementedError


def longest_common_subsequence(a: str, b: str) -> int:
    """LeetCode 1143. Длина наибольшей общей подпоследовательности.

    >>> longest_common_subsequence("abcde", "ace")
    3

    dp[i][j] — LCS префиксов a[:i] и b[:j].
    """
    raise NotImplementedError


def edit_distance(a: str, b: str) -> int:
    """LeetCode 72. Расстояние Левенштейна: минимум вставок, удалений и замен символа.

    >>> edit_distance("horse", "ros")
    3

    Где встречается в ML: метрики для распознавания речи (WER), исправление опечаток.
    """
    raise NotImplementedError


def unique_paths(m: int, n: int) -> int:
    """LeetCode 62. Число путей из левого верхнего угла сетки m x n в правый нижний,
    двигаясь только вправо и вниз.

    >>> unique_paths(3, 7)
    28
    """
    raise NotImplementedError
