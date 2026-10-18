"""Паттерн 9. Графы: BFS, DFS, топологическая сортировка, Дейкстра.

Первый шаг — понять, что это граф: сетка (клетки — вершины), зависимости
(курсы, пакеты), города и дороги. Второй — выбрать обход:
    BFS — кратчайший путь в невзвешенном графе;
    DFS — компоненты, обход всего, поиск циклов;
    топологическая сортировка — порядок с учётом зависимостей;
    Дейкстра — кратчайший путь с неотрицательными весами.
"""


def num_islands(grid: list[list[str]]) -> int:
    """LeetCode 200. Число островов ("1" — суша, "0" — вода, соседи по 4 направлениям).
    Входную сетку менять нельзя.

    >>> num_islands([["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]])
    2
    """
    raise NotImplementedError


def shortest_path_grid(grid: list[list[int]]) -> int:
    """LeetCode 1091. Кратчайший путь из левого верхнего угла в правый нижний по клеткам 0,
    ходы в 8 направлениях. Длина — число клеток пути; -1, если пути нет.

    >>> shortest_path_grid([[0, 1], [1, 0]])
    2

    Подумай: почему здесь BFS, а не DFS?
    """
    raise NotImplementedError


def course_order(num_courses: int, prerequisites: list[tuple[int, int]]) -> list[int]:
    """LeetCode 210. Порядок прохождения курсов 0..n-1; пара (a, b) значит «b перед a».
    Если порядка нет (цикл) — пустой список. Если вариантов несколько — с наименьшим
    доступным номером на каждом шаге.

    >>> course_order(4, [(1, 0), (2, 0), (3, 1), (3, 2)])
    [0, 1, 2, 3]

    Алгоритм Кана: берём вершины без входящих рёбер, удаляем их рёбра, повторяем.
    """
    raise NotImplementedError


def can_finish(num_courses: int, prerequisites: list[tuple[int, int]]) -> bool:
    """LeetCode 207. Можно ли пройти все курсы (нет ли циклических зависимостей)."""
    raise NotImplementedError


def count_components(n: int, edges: list[tuple[int, int]]) -> int:
    """LeetCode 323. Число компонент связности неориентированного графа с вершинами 0..n-1.

    >>> count_components(5, [(0, 1), (1, 2), (3, 4)])
    2
    """
    raise NotImplementedError


def network_delay(times: list[tuple[int, int, int]], n: int, source: int) -> int:
    """LeetCode 743. Сигнал идёт из source по рёбрам (u, v, время). За какое время он дойдёт
    до всех узлов 1..n? -1, если до кого-то не дойдёт.

    >>> network_delay([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2)
    2

    Алгоритм Дейкстры с кучей: O((V + E) log V).
    """
    raise NotImplementedError
