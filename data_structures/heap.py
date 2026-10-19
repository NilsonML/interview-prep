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
        self._data: list[Any] = []

    @classmethod
    def heapify(cls, items: list[Any]) -> "MinHeap":
        heap = cls()
        heap._data = list(items)
        # Листья (вторая половина массива) уже кучи из одного элемента.
        # Топим каждый внутренний узел снизу вверх: суммарно O(n).
        for i in range(len(heap._data) // 2 - 1, -1, -1):
            heap._sift_down(i)
        return heap

    def push(self, value: Any) -> None:
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> Any:
        if not self._data:
            raise IndexError("pop from empty heap")
        last = self._data.pop()
        if not self._data:
            return last
        top, self._data[0] = self._data[0], last
        self._sift_down(0)
        return top

    def peek(self) -> Any:
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    def __len__(self) -> int:
        return len(self._data)

    def _sift_up(self, i: int) -> None:
        data = self._data
        while i > 0:
            parent = (i - 1) // 2
            if data[i] >= data[parent]:
                break
            data[i], data[parent] = data[parent], data[i]
            i = parent

    def _sift_down(self, i: int) -> None:
        data, n = self._data, len(self._data)
        while True:
            smallest = i
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and data[child] < data[smallest]:
                    smallest = child
            if smallest == i:
                return
            data[i], data[smallest] = data[smallest], data[i]
            i = smallest
