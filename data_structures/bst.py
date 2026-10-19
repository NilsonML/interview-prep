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
