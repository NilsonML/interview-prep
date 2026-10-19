"""Система непересекающихся множеств (Union-Find, DSU).     [обязательно · неделя 7]

ИНТУИЦИЯ
    Компании и поглощения. У каждой компании есть «главный босс» (представитель).
    find(x) — дойти по цепочке начальников до главного. union(a, b) — одна компания
    поглощает другую: босс одной становится подчинённым босса другой.

КАК УСТРОЕНО: массив parent, корень указывает сам на себя
    parent = [0, 0, 1, 3]     0 <- 1 <- 2,  3 отдельно     -> множества {0,1,2}, {3}

    Две оптимизации дают почти O(1) на операцию (обратная функция Аккермана):
    1) сжатие путей: после find(2) все узлы пути смотрят прямо в корень: parent = [0,0,0,3];
    2) объединение по рангу: низкое дерево подвешиваем к высокому, а не наоборот.

ГДЕ ПРИМЕНЯЕТСЯ: компоненты связности, алгоритм Краскала, поиск циклов в графе,
кластеры дубликатов (как в async-dedup-pipeline).

ЗАДАНИЕ (элементы 0..n-1)
    - find(x) -> представитель, со сжатием путей;
    - union(a, b) -> bool: True, если множества были разными; по рангу или размеру;
    - connected(a, b) -> bool; атрибут count — текущее число множеств.
"""


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:  # сжатие путей: все узлы пути смотрят прямо в корень
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:  # низкое дерево подвешиваем к высокому
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)
