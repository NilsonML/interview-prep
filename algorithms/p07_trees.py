"""Паттерн 7. Деревья: DFS и BFS.

DFS (рекурсия или стек) — когда ответ собирается из ответов поддеревьев
(высота, диаметр, проверка свойства). BFS (очередь) — когда важны уровни.
Шаблон рекурсии: «что вернуть для пустого дерева?» + «как собрать ответ из детей?»
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
    raise NotImplementedError


def invert_tree(root: TreeNode | None) -> TreeNode | None:
    """LeetCode 226. Зеркально отразить дерево (на месте), вернуть корень."""
    raise NotImplementedError


def is_same_tree(p: TreeNode | None, q: TreeNode | None) -> bool:
    """LeetCode 100. Совпадают ли деревья по структуре и значениям."""
    raise NotImplementedError


def level_order(root: TreeNode | None) -> list[list[int]]:
    """LeetCode 102. Значения по уровням, слева направо.

    >>> level_order(from_level_order([3, 9, 20, None, None, 15, 7]))
    [[3], [9, 20], [15, 7]]
    """
    raise NotImplementedError


def is_valid_bst(root: TreeNode | None) -> bool:
    """LeetCode 98. Является ли дерево корректным BST (строгие неравенства).

    Ловушка: проверить только node.left.val < node.val < node.right.val недостаточно.
    [5, 1, 6, None, None, 3, 7] — не BST: 3 лежит в правом поддереве 5.
    """
    raise NotImplementedError


def lowest_common_ancestor_bst(root: TreeNode, p: int, q: int) -> int:
    """LeetCode 235. Значение наименьшего общего предка узлов со значениями p и q в BST.

    >>> lowest_common_ancestor_bst(from_level_order([6, 2, 8, 0, 4, 7, 9]), 2, 8)
    6

    Цель: O(h) без рекурсии по всему дереву — используй свойство BST.
    """
    raise NotImplementedError


def diameter(root: TreeNode | None) -> int:
    """LeetCode 543. Длина (в рёбрах) самого длинного пути между любыми двумя узлами.

    >>> diameter(from_level_order([1, 2, 3, 4, 5]))
    3

    Подумай: путь «перегибается» в каком-то узле. Что нужно знать о его поддеревьях?
    """
    raise NotImplementedError
