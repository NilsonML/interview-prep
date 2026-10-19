"""Хеш-таблица: как устроены dict и set.     [рекомендуется · неделя 1]

Сначала реши algorithms/p01_hashing.py обычным dict, потом загляни внутрь.

ИНТУИЦИЯ
    Гардероб в театре. Тебе дают номерок (hash), и куртку вешают на крючок с этим
    номером — искать среди всех курток не нужно. Иногда двум людям выпадает один
    крючок (коллизия): тогда на нём висят обе, и гардеробщик быстро перебирает пару курток.

КАК УСТРОЕНО (метод цепочек, separate chaining)
    buckets:  0: []
              1: [("cat", 3)]
              2: [("dog", 1), ("owl", 7)]   <- коллизия: обе пары в одной корзине
              3: []
    индекс корзины = hash(key) % capacity

    put("owl", 7):  hash("owl") % 4 == 2 -> идём в корзину 2 -> ключа нет -> добавляем пару.
    get("owl"):     та же корзина 2 -> перебираем 2 пары -> нашли.
    Пока в каждой корзине O(1) пар, все операции O(1).

    Рост (rehash): когда len / capacity > load factor (0.75), заводим вдвое больше корзин
    и ПЕРЕКЛАДЫВАЕМ каждый ключ заново: у hash % 8 и hash % 16 разные остатки.
    Рост в 2 раза -> перекладки редкие -> вставка O(1) амортизированно.

ТЕРМИНЫ
    hash-функция, коллизия, load factor, rehashing, амортизированная сложность,
    открытая адресация (так устроен dict в CPython: при коллизии ищем следующую свободную ячейку).

ТИПИЧНЫЕ ОШИБКИ
    - при put не проверить, что ключ уже есть -> дубликаты, неверный len;
    - при росте скопировать корзины как есть -> ключи «теряются» (ищутся не в той корзине);
    - сравнивать ключи через is вместо ==.

ЗАДАНИЕ: словарь без dict и set внутри, только на списках.
    - put / get / remove / __contains__ за O(1) в среднем;
    - при len / capacity > 0.75 таблица удваивается;
    - корректно при коллизиях (все ключи с одинаковым hash);
    - __iter__ отдаёт ключи, __len__ — число пар.

ПОДУМАЙ: почему ключ должен быть неизменяемым? Что сломается, если ключ поменять после put?
"""

from collections.abc import Hashable, Iterator
from typing import Any

LOAD_FACTOR = 0.75


class HashMap:
    def __init__(self, capacity: int = 8) -> None:
        raise NotImplementedError

    @property
    def capacity(self) -> int:
        raise NotImplementedError

    def put(self, key: Hashable, value: Any) -> None:
        raise NotImplementedError

    def get(self, key: Hashable, default: Any = None) -> Any:
        raise NotImplementedError

    def remove(self, key: Hashable) -> None:
        raise NotImplementedError

    def __contains__(self, key: Hashable) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[Hashable]:
        raise NotImplementedError
