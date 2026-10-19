"""Бинарная куча (min-heap) — как устроен heapq.     [рекомендуется · неделя 6]

Сначала реши algorithms/p08_heap.py с модулем heapq, потом загляни внутрь.

ИНТУИЦИЯ
    Турнирная сетка наоборот: каждый «начальник» не больше своих двух подчинённых.
    Поэтому самый маленький всегда наверху (в корне), а остальной порядок не важен.
    Это слабее сортировки — и поэтому дешевле: push и pop за O(log n), а не O(n).

КАК УСТРОЕНО: дерево хранится в обычном массиве, без указателей
    массив:  [1, 3, 2, 7, 4, 5]          дети i: 2i+1 и 2i+2, родитель i: (i-1)//2
    дерево:         1
                  /   \\
                 3     2
                / \\   /
               7   4 5

    push(0):  кладём в конец и «всплываем» (sift up): меняемся с родителем, пока он больше.
              [1,3,2,7,4,5,0] -> 0 меняется с 2 -> с 1 -> [0,3,1,7,4,5,2]
    pop():    достаём корень, на его место — последний элемент, и он «тонет» (sift down):
              меняется с МЕНЬШИМ из детей, пока больше кого-то из них.
    Высота дерева log n -> оба пути O(log n).

    heapify за O(n): топим узлы снизу вверх. Половина узлов — листья (тонуть некуда),
    четверть тонет на 1 уровень, восьмая на 2 ... сумма — O(n).

ТЕРМИНЫ
    min-heap / max-heap, sift up / sift down, heapify, приоритетная очередь.
    В Python heapq — только min-heap; max-heap делают через отрицание: heappush(h, -x).

ТИПИЧНЫЕ ОШИБКИ
    - при sift down менять с любым ребёнком, а не с меньшим -> свойство кучи ломается;
    - забыть случай, когда pop делают из кучи из одного элемента.

ЗАДАНИЕ (без heapq)
    - push O(log n); pop() -> минимум O(log n), IndexError на пустой; peek() O(1);
    - classmethod heapify(items) -> MinHeap за O(n), входной список не менять;
    - __len__.
"""

from typing import Any


class MinHeap:
    def __init__(self) -> None:
        raise NotImplementedError

    @classmethod
    def heapify(cls, items: list[Any]) -> "MinHeap":
        raise NotImplementedError

    def push(self, value: Any) -> None:
        raise NotImplementedError

    def pop(self) -> Any:
        raise NotImplementedError

    def peek(self) -> Any:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
