"""Лаба 1. Поиск в list против set.

ПРЕДСКАЖИ ДО ЗАПУСКА (запиши в JOURNAL.md):
    1. Как изменится время `x in list`, если n вырастет в 10 раз? А `x in set`?
    2. При n = 1 000 000 во сколько раз set быстрее: в 10, 1 000 или 100 000 раз?

Почему ищем последний элемент: это худший случай для list (просмотр всех n).
"""

import timeit


def main() -> None:
    print(f"{'n':>10} {'list, мкс':>12} {'set, мкс':>10} {'во сколько раз':>16}")
    for n in (10**3, 10**4, 10**5, 10**6):
        data = list(range(n))
        as_set = set(data)
        x = n - 1
        t_list = min(timeit.repeat(lambda x=x, data=data: x in data, number=20, repeat=3)) / 20
        t_set = min(timeit.repeat(lambda x=x, s=as_set: x in s, number=20, repeat=3)) / 20
        print(f"{n:>10} {t_list * 1e6:>12.1f} {t_set * 1e6:>10.3f} {t_list / t_set:>16.0f}")
    print("\nВывод: время list растёт ~линейно (O(n)), set почти не меняется (O(1)).")


if __name__ == "__main__":
    main()
