"""Система непересекающихся множеств (Union-Find, DSU).

Задание: реализуй DSU для элементов 0..n-1.

Требования:
    - find(x) -> представитель множества, со сжатием путей;
    - union(a, b) -> bool: True, если множества были разными и объединились;
      объединение по рангу (или размеру);
    - connected(a, b) -> bool;
    - count: текущее число множеств;
    - обе оптимизации вместе дают почти O(1) на операцию (обратная функция Аккермана).

Где применяется: компоненты связности, алгоритм Краскала, поиск циклов в графе,
кластеризация дублей (как в async-dedup-pipeline).
"""


class UnionFind:
    def __init__(self, n: int) -> None:
        raise NotImplementedError

    def find(self, x: int) -> int:
        raise NotImplementedError

    def union(self, a: int, b: int) -> bool:
        raise NotImplementedError

    def connected(self, a: int, b: int) -> bool:
        raise NotImplementedError
