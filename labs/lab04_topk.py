"""Лаба 4. Top-k: heapq против сортировки.

ПРЕДСКАЖИ ДО ЗАПУСКА:
    1. Что быстрее при n = 10^6, k = 10: sorted(...)[-k:] или heapq.nlargest(k, ...)?
    2. А при k = n / 2? Почему ответ может поменяться?
Подсказка: O(n log k) против O(n log n), но константы у встроенной сортировки очень малы.
"""

import heapq
import random
import timeit


def main() -> None:
    data = [random.random() for _ in range(1_000_000)]
    print(f"{'k':>8} {'sorted, с':>10} {'nlargest, с':>12}")
    for k in (10, 1_000, 500_000):
        t_sort = min(timeit.repeat(lambda k=k: sorted(data)[-k:], number=1, repeat=3))
        t_heap = min(timeit.repeat(lambda k=k: heapq.nlargest(k, data), number=1, repeat=3))
        print(f"{k:>8} {t_sort:>10.3f} {t_heap:>12.3f}")
    print("\nВывод: асимптотика — не всё. При большом k сортировка на C обгоняет кучу.")


if __name__ == "__main__":
    main()
