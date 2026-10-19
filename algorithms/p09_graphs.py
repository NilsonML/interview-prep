"""Паттерн 9. Графы.     [неделя 7]

СИГНАЛЫ: сетка (клетки — вершины, соседи — рёбра), зависимости (курсы, пакеты),
«связаны ли», «кратчайший путь», «сколько групп».

КАКОЙ ОБХОД:
    BFS (очередь)        — кратчайший путь, когда все рёбра одинаковой длины (волна от источника);
    DFS (стек/рекурсия)  — обойти всё, компоненты, циклы;
    Кан / топосорт       — порядок с учётом зависимостей; если не все вершины вошли — есть цикл;
    Дейкстра (куча)      — кратчайший путь с неотрицательными весами;
    Union-Find           — «объединить и проверить связность» по рёбрам.

ЛОВУШКИ: помечай вершину посещённой при ДОБАВЛЕНИИ в очередь, а не при извлечении;
рекурсивный DFS на большой сетке упирается в лимит глубины — используй явный стек.
"""

import heapq
from collections import defaultdict, deque


def num_islands(grid: list[list[str]]) -> int:
    """LeetCode 200. Число островов ("1" — суша, "0" — вода, соседи по 4 направлениям).
    Входную сетку менять нельзя.

    >>> num_islands([["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]])
    2
    """
    rows, cols = len(grid), len(grid[0]) if grid else 0
    seen: set[tuple[int, int]] = set()
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                count += 1
                stack = [(r, c)]  # итеративный DFS: большая сетка не упрётся в лимит рекурсии
                seen.add((r, c))
                while stack:
                    i, j = stack.pop()
                    for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                        if (
                            0 <= ni < rows
                            and 0 <= nj < cols
                            and grid[ni][nj] == "1"
                            and (ni, nj) not in seen
                        ):
                            seen.add((ni, nj))
                            stack.append((ni, nj))
    return count


def shortest_path_grid(grid: list[list[int]]) -> int:
    """LeetCode 1091. Кратчайший путь из левого верхнего угла в правый нижний по клеткам 0,
    ходы в 8 направлениях. Длина — число клеток пути; -1, если пути нет.

    >>> shortest_path_grid([[0, 1], [1, 0]])
    2

    Подумай: почему здесь BFS, а не DFS?
    """
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    queue = deque([(0, 0, 1)])
    seen = {(0, 0)}
    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == (n - 1, n - 1):
            return dist  # BFS идёт волнами: первое достижение — кратчайшее
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and not grid[nr][nc] and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
    return -1


def course_order(num_courses: int, prerequisites: list[tuple[int, int]]) -> list[int]:
    """LeetCode 210. Порядок прохождения курсов 0..n-1; пара (a, b) значит «b перед a».
    Если порядка нет (цикл) — пустой список. Если вариантов несколько — с наименьшим
    доступным номером на каждом шаге.

    >>> course_order(4, [(1, 0), (2, 0), (3, 1), (3, 2)])
    [0, 1, 2, 3]

    Алгоритм Кана: берём вершины без входящих рёбер, удаляем их рёбра, повторяем.
    """
    graph: dict[int, list[int]] = defaultdict(list)
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    ready = [c for c in range(num_courses) if indegree[c] == 0]
    heapq.heapify(ready)  # куча вместо очереди: на каждом шаге наименьший номер
    order = []
    while ready:
        node = heapq.heappop(ready)
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                heapq.heappush(ready, nxt)
    return order if len(order) == num_courses else []  # не все вошли -> есть цикл


def can_finish(num_courses: int, prerequisites: list[tuple[int, int]]) -> bool:
    """LeetCode 207. Можно ли пройти все курсы (нет ли циклических зависимостей)."""
    return len(course_order(num_courses, prerequisites)) == num_courses


def count_components(n: int, edges: list[tuple[int, int]]) -> int:
    """LeetCode 323. Число компонент связности неориентированного графа с вершинами 0..n-1.

    >>> count_components(5, [(0, 1), (1, 2), (3, 4)])
    2
    """
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # сжатие пути вдвое
            x = parent[x]
        return x

    components = n
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            components -= 1
    return components


def network_delay(times: list[tuple[int, int, int]], n: int, source: int) -> int:
    """LeetCode 743. Сигнал идёт из source по рёбрам (u, v, время). За какое время он дойдёт
    до всех узлов 1..n? -1, если до кого-то не дойдёт.

    >>> network_delay([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2)
    2

    Алгоритм Дейкстры с кучей: O((V + E) log V).
    """
    graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    dist: dict[int, int] = {}
    heap = [(0, source)]
    while heap:
        d, node = heapq.heappop(heap)
        if node in dist:
            continue  # уже нашли путь короче (в куче остался устаревший)
        dist[node] = d
        for nxt, w in graph[node]:
            if nxt not in dist:
                heapq.heappush(heap, (d + w, nxt))
    return max(dist.values()) if len(dist) == n else -1
