"""Паттерн 11. Динамическое программирование.     [недели 9–10]

СИГНАЛЫ: «минимум / максимум / число способов», выбор на каждом шаге влияет на
следующие, а перебор экспоненциальный.

ИДЕЯ: большая задача = комбинация меньших, и меньшие повторяются. Решаем каждую
подзадачу один раз и запоминаем.
Аналогия: считать ступеньки по одной глупо, если помнишь, сколько способов было
дойти до двух предыдущих.

РЕЦЕПТ
    1. Состояние: что значит dp[i] (dp[i][j])? Сформулируй СЛОВАМИ.
    2. Переход: как dp[i] выражается через меньшие состояния?
    3. База: самые маленькие состояния.
    4. Порядок вычисления и где лежит ответ.
Начинай сверху вниз (рекурсия + @functools.cache), потом переписывай в таблицу и
сжимай память до одной строки.
"""


def climb_stairs(n: int) -> int:
    """LeetCode 70. Число способов подняться на n ступенек шагами по 1 или 2.

    >>> climb_stairs(3)
    3

    dp[i] = dp[i-1] + dp[i-2]. Цель: O(n) времени, O(1) памяти.
    """
    a, b = 1, 1  # способы для ступенек i-2 и i-1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def rob(houses: list[int]) -> int:
    """LeetCode 198. Максимальная сумма без двух соседних домов.

    >>> rob([2, 7, 9, 3, 1])
    12
    """
    take, skip = 0, 0  # лучшая сумма, если текущий дом взят / не взят
    for money in houses:
        take, skip = skip + money, max(take, skip)
    return max(take, skip)


def coin_change(coins: list[int], amount: int) -> int:
    """LeetCode 322. Минимальное число монет на сумму amount (монет каждого номинала
    сколько угодно); -1, если нельзя.

    >>> coin_change([1, 2, 5], 11)
    3

    Подумай: почему жадный алгоритм «берём самую крупную» ошибается на [1, 3, 4], 6?
    """
    inf = amount + 1  # больше любого возможного ответа
    dp = [0] + [inf] * amount  # dp[s] — минимум монет на сумму s
    for s in range(1, amount + 1):
        for coin in coins:
            if coin <= s:
                dp[s] = min(dp[s], dp[s - coin] + 1)
    return dp[amount] if dp[amount] != inf else -1


def length_of_lis(nums: list[int]) -> int:
    """LeetCode 300. Длина наибольшей строго возрастающей подпоследовательности.

    >>> length_of_lis([10, 9, 2, 5, 3, 7, 101, 18])
    4

    Сначала O(n^2): dp[i] — длина LIS, заканчивающейся в i. Бонус: O(n log n).
    """
    # O(n log n): tails[k] — наименьший возможный хвост возрастающей последовательности длины k+1
    tails: list[int] = []
    for x in nums:
        lo, hi = 0, len(tails)
        while lo < hi:  # lower_bound из паттерна 5
            mid = (lo + hi) // 2
            if tails[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(x)
        else:
            tails[lo] = x
    return len(tails)


def longest_common_subsequence(a: str, b: str) -> int:
    """LeetCode 1143. Длина наибольшей общей подпоследовательности.

    >>> longest_common_subsequence("abcde", "ace")
    3

    dp[i][j] — LCS префиксов a[:i] и b[:j].
    """
    prev = [0] * (len(b) + 1)  # храним только предыдущую строку таблицы: O(len(b)) памяти
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]


def edit_distance(a: str, b: str) -> int:
    """LeetCode 72. Расстояние Левенштейна: минимум вставок, удалений и замен символа.

    >>> edit_distance("horse", "ros")
    3

    Где встречается в ML: метрики для распознавания речи (WER), исправление опечаток.
    """
    prev = list(range(len(b) + 1))  # из пустой a в b[:j] — j вставок
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])  # удалить, вставить, заменить
        prev = cur
    return prev[-1]


def unique_paths(m: int, n: int) -> int:
    """LeetCode 62. Число путей из левого верхнего угла сетки m x n в правый нижний,
    двигаясь только вправо и вниз.

    >>> unique_paths(3, 7)
    28
    """
    row = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]  # сверху (старое row[j]) + слева (новое row[j-1])
    return row[-1]
