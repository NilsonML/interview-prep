"""Предскажи результат: структуры данных и алгоритмы «вручную».     [недели 3–9]

Трассировка — проследить состояние структуры шаг за шагом — главный способ понять,
как она работает. Рисуй на бумаге: массив кучи, очередь BFS, стек DFS, таблицу DP.
Порядок работы такой же, как в python_basics.py: сначала ответ в ANSWERS, потом тест.
"""

import heapq
from collections import Counter, deque


def q01():
    """Массив кучи после вставок (heapq — min-heap)."""
    h = []
    for x in [5, 3, 8, 1]:
        heapq.heappush(h, x)
    return h


def q02():
    """Порядок извлечения из кучи кортежей (приоритет, имя)."""
    h = []
    for task in [(2, "write"), (1, "read"), (2, "deploy"), (0, "plan")]:
        heapq.heappush(h, task)
    return [heapq.heappop(h)[1] for _ in range(4)]


def q03():
    """Операции deque."""
    d = deque([1, 2, 3])
    d.rotate(1)
    d.appendleft(0)
    d.pop()
    return list(d)


GRAPH = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["F"], "E": ["F"], "F": []}


def q04():
    """Порядок обхода BFS из A (соседи в порядке списка)."""
    order, queue, seen = [], deque(["A"]), {"A"}
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in GRAPH[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return order


def q05():
    """Порядок обхода DFS на явном стеке из A. Сравни с рекурсивным DFS!"""
    order, stack, seen = [], ["A"], set()
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        for nxt in GRAPH[node]:
            stack.append(nxt)
    return order


def q06():
    """Прямой обход (preorder: узел, левое, правое) BST после вставок."""
    tree: dict = {}  # узел -> [left, right]
    root = None
    for key in [5, 3, 8, 1, 4, 9]:
        if root is None:
            root = key
            tree[key] = [None, None]
            continue
        node = root
        while True:
            side = 0 if key < node else 1
            if tree[node][side] is None:
                tree[node][side] = key
                tree[key] = [None, None]
                break
            node = tree[node][side]

    def preorder(node):
        return [] if node is None else [node, *preorder(tree[node][0]), *preorder(tree[node][1])]

    return preorder(root)


def q07():
    """Какие mid посетит lower_bound (шаблон [lo, hi)) при поиске 7?"""
    nums, target = [1, 3, 5, 7, 9, 11], 7
    lo, hi, mids = 0, len(nums), []
    while lo < hi:
        mid = (lo + hi) // 2
        mids.append(mid)
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return mids, lo


def q08():
    """Состояние монотонного стека (индексы) после каждого элемента."""
    temps = [73, 74, 71, 69, 72]
    stack, states = [], []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            stack.pop()
        stack.append(i)
        states.append(list(stack))
    return states


def q09():
    """Таблица DP: число способов подняться на n ступенек шагами 1 и 2."""
    n = 5
    dp = [1, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp


def q10():
    """Counter.most_common при равных частотах."""
    return Counter("abracadabra").most_common(3)


def q11():
    """Устойчивость сортировки."""
    words = ["bb", "a", "cc", "d", "aa"]
    return sorted(words, key=len)


def q12():
    """Указатели двух сумм: какие пары (left, right) будут проверены?"""
    nums, target = [1, 2, 4, 6, 10], 8
    left, right, checked = 0, len(nums) - 1, []
    while left < right:
        checked.append((left, right))
        s = nums[left] + nums[right]
        if s == target:
            break
        if s < target:
            left += 1
        else:
            right -= 1
    return checked


# Впиши ответы вместо ... (Ellipsis). Код не запускай — в этом весь смысл.
ANSWERS = {
    "q01": ...,
    "q02": ...,
    "q03": ...,
    "q04": ...,
    "q05": ...,
    "q06": ...,
    "q07": ...,
    "q08": ...,
    "q09": ...,
    "q10": ...,
    "q11": ...,
    "q12": ...,
}
