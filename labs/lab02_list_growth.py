"""Лаба 2. Как растут list и dict.

ПРЕДСКАЖИ ДО ЗАПУСКА:
    1. Растёт ли ёмкость list на каждом append? Если нет — на сколько за раз?
    2. На каком по счёту элементе dict впервые увеличит таблицу?

sys.getsizeof показывает выделенную память; её скачки = перевыделения.
"""

import sys


def growth_points(make, add, limit: int) -> list[tuple[int, int]]:
    obj = make()
    last, points = sys.getsizeof(obj), []
    for i in range(limit):
        add(obj, i)
        size = sys.getsizeof(obj)
        if size != last:
            points.append((i + 1, size))
            last = size
    return points


def main() -> None:
    print("list: (длина после append, байт)")
    print(growth_points(list, lambda o, i: o.append(i), 100))
    print("\ndict: (число ключей после вставки, байт)")
    print(growth_points(dict, lambda o, i: o.__setitem__(i, i), 200))
    print(
        "\nВывод: перевыделения всё реже -> вставка O(1) амортизированно. "
        "Сравни шаги роста list и dict."
    )


if __name__ == "__main__":
    main()
