"""Почини баг: алгоритмы.     [недели 1–9]

Порядок работы как в python_bugs.py: воспроизведи -> исправь минимально ->
комментарий «# БАГ: ... ИСПРАВЛЕНИЕ: ...» -> FIXED["имя"] = True -> pytest.

Совет: баги в алгоритмах почти всегда на границах. Проверь пустой вход, один элемент,
все одинаковые, ответ в самом начале и в самом конце.
"""

FIXED = {
    "binary_search": False,
    "two_sum": False,
    "max_profit": False,
    "is_valid_brackets": False,
    "merge_intervals": False,
    "longest_unique_substring": False,
    "count_islands": False,
    "coin_change": False,
}


def binary_search(nums: list[int], target: int) -> int:
    """Индекс target в отсортированном массиве или -1.

    Жалоба: «binary_search([1, 3, 5], 7) падает с IndexError».
    """
    lo, hi = 0, len(nums)
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    """Индексы i < j с суммой target (решение существует).

    Жалоба: «two_sum([3, 2, 4], 6) возвращает (0, 0) — один и тот же элемент дважды».
    """
    seen: dict[int, int] = {}
    for j, x in enumerate(nums):
        seen[x] = j
        if target - x in seen:
            return seen[target - x], j
    raise ValueError("no solution")


def max_profit(prices: list[int]) -> int:
    """Максимальная прибыль от одной покупки и одной более поздней продажи (или 0).

    Жалоба: «Для [7, 5, 6] выдаёт 7, хотя купить за 5 и продать за 6 — это 1».
    """
    min_price = 0
    best = 0
    for p in prices:
        min_price = min(min_price, p)
        best = max(best, p - min_price)
    return best


def is_valid_brackets(s: str) -> bool:
    """Правильная ли скобочная последовательность из ()[]{}.

    Жалоба: «"((" считается правильной».
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return True


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Слить пересекающиеся интервалы. Входной список не менять.

    Жалоба: «[[5, 6], [1, 2]] сливается неправильно, а [[1, 10], [2, 3]] даёт [[1, 3]]».
    Здесь два бага.
    """
    result: list[list[int]] = []
    for start, end in intervals:
        if result and start <= result[-1][1]:
            result[-1][1] = end
        else:
            result.append([start, end])
    return result


def longest_unique_substring(s: str) -> int:
    """Длина самой длинной подстроки без повторяющихся символов.

    Жалоба: «Для "abba" выдаёт 3, хотя ответ 2».
    """
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last_seen:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


def count_islands(grid: list[list[str]]) -> int:
    """Число островов из "1" (соседи по 4 направлениям). Сетку не менять.

    Жалоба: «На любой сетке с сушей падает RecursionError».
    """
    rows, cols = len(grid), len(grid[0]) if grid else 0
    seen: set[tuple[int, int]] = set()

    def dfs(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            dfs(r + dr, c + dc)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                count += 1
                dfs(r, c)
    return count


def coin_change(coins: list[int], amount: int) -> int:
    """Минимальное число монет на сумму amount (монет каждого номинала сколько угодно),
    -1, если нельзя.

    Жалоба: «coin_change([1, 3, 4], 6) возвращает 3, хотя 3 + 3 — это 2 монеты».
    Подсказка: это не опечатка, а неверный выбор алгоритма.
    """
    count = 0
    for coin in sorted(coins, reverse=True):
        take = amount // coin
        count += take
        amount -= take * coin
    return count if amount == 0 else -1
