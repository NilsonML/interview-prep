"""Бинарное дерево поиска (BST).     [опционально (удаление) · неделя 5]

ИНТУИЦИЯ
    Игра «угадай число»: на каждом узле спрашиваем «меньше или больше?» и отбрасываем
    половину. Слева от узла всё меньше, справа — всё больше.

КАК УСТРОЕНО
             50
           /    \\
         30      70
        /  \\    /  \\
      20   40  60   80

    contains(60):  60 > 50 -> вправо; 60 < 70 -> влево; нашли. Путь = высота дерева h.
    inorder (левое -> узел -> правое) выдаёт ключи ПО ВОЗРАСТАНИЮ: 20 30 40 50 60 70 80.
    remove(50), у узла два ребёнка: ставим на его место преемника — минимум правого
    поддерева (60), и удаляем 60 из правого поддерева (у него максимум один ребёнок).

    Все операции O(h). Сбалансированное дерево: h = log n. Вставка 1, 2, 3, ..., n по
    порядку даёт «палку» высотой n -> O(n). Поэтому в реальных системах деревья
    балансируют (красно-чёрное, AVL; B-дерево — индексы в базах данных).

ТЕРМИНЫ: inorder / preorder / postorder, высота, преемник (successor), балансировка.

ТИПИЧНЫЕ ОШИБКИ
    - проверять BST только по соседям (левый ребёнок < узел), а не по всему поддереву;
    - рекурсия на вырожденном дереве упирается в лимит глубины Python (1000).

ЗАДАНИЕ: множество на BST без балансировки.
    - insert(key), дубликаты игнорируются; __contains__(key);
    - remove(key), KeyError если нет: случаи «лист», «один ребёнок», «два ребёнка»;
    - min() / max(), ValueError на пустом;
    - inorder() -> list по возрастанию; height(): пустое 0, один узел 1; __len__.
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
        self.root: TreeNode | None = None
        self._size = 0

    def insert(self, key: Any) -> None:
        if self.root is None:
            self.root = TreeNode(key)
            self._size += 1
            return
        node = self.root
        while True:  # итеративно: нет риска упереться в лимит рекурсии на вырожденном дереве
            if key == node.key:
                return
            side = "left" if key < node.key else "right"
            child = getattr(node, side)
            if child is None:
                setattr(node, side, TreeNode(key))
                self._size += 1
                return
            node = child

    def __contains__(self, key: Any) -> bool:
        node = self.root
        while node is not None:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def remove(self, key: Any) -> None:
        if key not in self:
            raise KeyError(key)
        self.root = self._remove(self.root, key)
        self._size -= 1

    def _remove(self, node: TreeNode | None, key: Any) -> TreeNode | None:
        if node is None:
            return None
        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            if node.left is None:  # лист или только правый ребёнок
                return node.right
            if node.right is None:  # только левый ребёнок
                return node.left
            # Два ребёнка: преемник — минимум правого поддерева (больше всех слева,
            # меньше всех остальных справа), ставим его ключ сюда и удаляем его там.
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key = successor.key
            node.right = self._remove(node.right, successor.key)
        return node

    def min(self) -> Any:
        if self.root is None:
            raise ValueError("empty tree")
        node = self.root
        while node.left is not None:
            node = node.left
        return node.key

    def max(self) -> Any:
        if self.root is None:
            raise ValueError("empty tree")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.key

    def inorder(self) -> list[Any]:
        # Обход "левое -> узел -> правое" на явном стеке: в BST даёт отсортированный порядок
        result, stack, node = [], [], self.root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.key)
            node = node.right
        return result

    def height(self) -> int:
        # BFS по уровням: высота = число уровней
        level, height = [self.root] if self.root else [], 0
        while level:
            height += 1
            level = [c for n in level for c in (n.left, n.right) if c is not None]
        return height

    def __len__(self) -> int:
        return self._size
