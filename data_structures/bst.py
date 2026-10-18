"""Бинарное дерево поиска (BST).

Задание: реализуй множество на BST (без балансировки).

Свойство BST: все ключи в левом поддереве меньше узла, в правом — больше.

Требования:
    - insert(key): дубликаты игнорируются;
    - __contains__(key);
    - remove(key): KeyError, если нет. Три случая: лист, один ребёнок, два ребёнка
      (замени на минимум правого поддерева);
    - min() / max(): ValueError на пустом;
    - inorder() -> list: ключи по возрастанию;
    - height(): пустое дерево — 0, один узел — 1;
    - __len__.

Подумай до кода:
    - Все операции стоят O(h). Какая h у дерева, если вставлять 1, 2, 3, ..., n по порядку?
      Поэтому в реальных системах используют сбалансированные деревья (красно-чёрное, B-дерево).
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TreeNode:
    key: Any
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


class BST:
    def __init__(self) -> None:
        raise NotImplementedError

    def insert(self, key: Any) -> None:
        raise NotImplementedError

    def __contains__(self, key: Any) -> bool:
        raise NotImplementedError

    def remove(self, key: Any) -> None:
        raise NotImplementedError

    def min(self) -> Any:
        raise NotImplementedError

    def max(self) -> Any:
        raise NotImplementedError

    def inorder(self) -> list[Any]:
        raise NotImplementedError

    def height(self) -> int:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
