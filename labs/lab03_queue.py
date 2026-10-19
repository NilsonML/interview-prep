"""Лаба 3. Очередь на list против collections.deque.

ПРЕДСКАЖИ ДО ЗАПУСКА:
    1. Обработать очередь из n элементов через list.pop(0) — это O(?) суммарно?
    2. Во сколько раз deque быстрее при n = 100 000?
"""

import time
from collections import deque


def drain_list(n: int) -> float:
    queue = list(range(n))
    start = time.perf_counter()
    while queue:
        queue.pop(0)  # сдвигает все оставшиеся элементы влево: O(n)
    return time.perf_counter() - start


def drain_deque(n: int) -> float:
    queue = deque(range(n))
    start = time.perf_counter()
    while queue:
        queue.popleft()  # O(1)
    return time.perf_counter() - start


def main() -> None:
    print(f"{'n':>8} {'list.pop(0), с':>16} {'deque, с':>10}")
    for n in (10_000, 50_000, 100_000):
        print(f"{n:>8} {drain_list(n):>16.3f} {drain_deque(n):>10.4f}")
    print(
        "\nВывод: list растёт квадратично (n раз по O(n)), deque — линейно. BFS — только на deque."
    )


if __name__ == "__main__":
    main()
