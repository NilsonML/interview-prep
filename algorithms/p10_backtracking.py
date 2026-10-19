"""Паттерн 10. Перебор с возвратом (backtracking).     [неделя 8]

СИГНАЛЫ: «все подмножества / перестановки / комбинации», «все способы», n <= 20.

ИДЕЯ: обход дерева решений. На каждом уровне делаем выбор, идём глубже, потом
отменяем выбор и пробуем следующий. Отсечения (pruning) обрезают ветки, которые
точно не приведут к ответу.
Аналогия: лабиринт — дошёл до тупика, вернулся к последней развилке.

ШАБЛОН
    def backtrack(состояние):
        if решение готово: сохранить КОПИЮ; return
        for выбор in варианты:
            if выбор допустим:
                сделать выбор; backtrack(...); отменить выбор
"""


def subsets(nums: list[int]) -> list[list[int]]:
    """LeetCode 78. Все подмножества (элементы уникальны). Порядок: каждое подмножество
    сохраняет порядок исходного массива, список подмножеств отсортирован.

    >>> subsets([1, 2])
    [[], [1], [1, 2], [2]]
    """
    result: list[list[int]] = []
    path: list[int] = []

    def backtrack(start: int) -> None:
        result.append(path.copy())  # copy: path продолжит меняться
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return sorted(result)


def permutations(nums: list[int]) -> list[list[int]]:
    """LeetCode 46. Все перестановки (элементы уникальны), отсортированный список.

    >>> permutations([1, 2, 3])
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

    Без itertools.permutations.
    """
    result: list[list[int]] = []
    path: list[int] = []
    used = [False] * len(nums)

    def backtrack() -> None:
        if len(path) == len(nums):
            result.append(path.copy())
            return
        for i, x in enumerate(nums):
            if not used[i]:
                used[i] = True
                path.append(x)
                backtrack()
                path.pop()
                used[i] = False

    backtrack()
    return sorted(result)


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """LeetCode 39. Все уникальные комбинации из candidates (положительные, уникальные),
    дающие в сумме target; число можно брать сколько угодно раз. Каждая комбинация
    отсортирована, список комбинаций отсортирован.

    >>> combination_sum([2, 3, 6, 7], 7)
    [[2, 2, 3], [7]]
    """
    candidates = sorted(candidates)
    result: list[list[int]] = []
    path: list[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(path.copy())
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # дальше только больше — отсечение
            path.append(candidates[i])
            backtrack(i, remaining - candidates[i])  # i, а не i+1: число можно повторить
            path.pop()

    backtrack(0, target)
    return result


def generate_parentheses(n: int) -> list[str]:
    """LeetCode 22. Все правильные скобочные последовательности из n пар, по алфавиту.

    >>> generate_parentheses(2)
    ['(())', '()()']
    """
    result: list[str] = []

    def backtrack(current: str, opened: int, closed: int) -> None:
        if len(current) == 2 * n:
            result.append(current)
            return
        if opened < n:
            backtrack(current + "(", opened + 1, closed)
        if closed < opened:  # закрыть можно, только если есть незакрытая
            backtrack(current + ")", opened, closed + 1)

    backtrack("", 0, 0)
    return result


def word_search(board: list[list[str]], word: str) -> bool:
    """LeetCode 79. Можно ли составить word, двигаясь по соседним (4 направления) клеткам,
    не используя клетку дважды. Входную доску после работы вернуть в исходное состояние.

    >>> word_search([["A", "B"], ["C", "D"]], "ABD")
    True
    """
    rows, cols = len(board), len(board[0])

    def backtrack(r: int, c: int, i: int) -> bool:
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
            return False
        saved, board[r][c] = board[r][c], "#"  # помечаем как использованную
        found = any(
            backtrack(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
        )
        board[r][c] = saved  # возврат
        return found

    return any(backtrack(r, c, 0) for r in range(rows) for c in range(cols))
