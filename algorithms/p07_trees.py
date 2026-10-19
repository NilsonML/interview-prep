"""Паттерн 7. Деревья: DFS и BFS.     [неделя 5]

СИГНАЛЫ: дан TreeNode; «глубина», «путь», «по уровням», «проверить свойство дерева».

ИДЕЯ DFS (рекурсия): доверься рекурсии. Ответ для дерева = f(ответ для левого,
ответ для правого, сам узел). Два вопроса: что вернуть для None? как собрать ответ из детей?
ИДЕЯ BFS (очередь): обход по уровням — «волны» от корня. len(queue) в начале
итерации = число узлов на текущем уровне.

ЛОВУШКА: иногда функция должна ВЕРНУТЬ одно (высоту), а ОТВЕТ копить другой
(диаметр = max по узлам левая высота + правая). Тогда ответ держи в nonlocal.
"""

from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def from_level_order(values: list[int | None]) -> TreeNode | None:
    """Вспомогательная: дерево из записи по уровням как на LeetCode, None — нет узла.
    [3, 9, 20, None, None, 15, 7] ->    3
                                       / \\
                                      9   20
                                         /  \\
                                        15   7
    Уже реализована.
    """
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        for side in ("left", "right"):
            if i < len(values) and values[i] is not None:
                child = TreeNode(values[i])
                setattr(node, side, child)
                queue.append(child)
            i += 1
    return root


def max_depth(root: TreeNode | None) -> int:
    """LeetCode 104. Максимальная глубина (число узлов на самом длинном пути от корня).

    >>> max_depth(from_level_order([3, 9, 20, None, None, 15, 7]))
    3
    """
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def invert_tree(root: TreeNode | None) -> TreeNode | None:
    """LeetCode 226. Зеркально отразить дерево (на месте), вернуть корень."""
    if root is not None:
        root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


def is_same_tree(p: TreeNode | None, q: TreeNode | None) -> bool:
    """LeetCode 100. Совпадают ли деревья по структуре и значениям."""
    if p is None or q is None:
        return p is q
    return p.val == q.val and is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)


def level_order(root: TreeNode | None) -> list[list[int]]:
    """LeetCode 102. Значения по уровням, слева направо.

    >>> level_order(from_level_order([3, 9, 20, None, None, 15, 7]))
    [[3], [9, 20], [15, 7]]
    """
    if root is None:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):  # ровно столько узлов, сколько на текущем уровне
            node = queue.popleft()
            level.append(node.val)
            queue.extend(c for c in (node.left, node.right) if c is not None)
        result.append(level)
    return result


def is_valid_bst(root: TreeNode | None) -> bool:
    """LeetCode 98. Является ли дерево корректным BST (строгие неравенства).

    Ловушка: проверить только node.left.val < node.val < node.right.val недостаточно.
    [5, 1, 6, None, None, 3, 7] — не BST: 3 лежит в правом поддереве 5.
    """

    def check(node: TreeNode | None, low: float, high: float) -> bool:
        if node is None:
            return True
        if not low < node.val < high:
            return False
        return check(node.left, low, node.val) and check(node.right, node.val, high)

    return check(root, float("-inf"), float("inf"))


def lowest_common_ancestor_bst(root: TreeNode, p: int, q: int) -> int:
    """LeetCode 235. Значение наименьшего общего предка узлов со значениями p и q в BST.

    >>> lowest_common_ancestor_bst(from_level_order([6, 2, 8, 0, 4, 7, 9]), 2, 8)
    6

    Цель: O(h) без рекурсии по всему дереву — используй свойство BST.
    """
    node = root
    while True:
        if p < node.val and q < node.val:
            node = node.left
        elif p > node.val and q > node.val:
            node = node.right
        else:  # p и q расходятся (или один из них — сам node)
            return node.val


def diameter(root: TreeNode | None) -> int:
    """LeetCode 543. Длина (в рёбрах) самого длинного пути между любыми двумя узлами.

    >>> diameter(from_level_order([1, 2, 3, 4, 5]))
    3

    Подумай: путь «перегибается» в каком-то узле. Что нужно знать о его поддеревьях?
    """
    best = 0

    def height(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left, right = height(node.left), height(node.right)
        best = max(best, left + right)  # путь через node
        return 1 + max(left, right)

    height(root)
    return best
