"""Хеш-таблица с цепочками (separate chaining).

Задание: реализуй словарь без использования dict и set внутри, только на списках.

Требования:
    - put / get / remove / __contains__ за O(1) в среднем;
    - при коэффициенте заполнения len / capacity > 0.75 таблица удваивается;
    - корректная работа при коллизиях (все ключи с одинаковым hash);
    - __iter__ отдаёт ключи, __len__ — число пар.

Подумай до кода:
    - Почему при увеличении таблицы нельзя просто скопировать корзины по порядку?
    - Почему ключ должен быть неизменяемым?

Теория: урок 1 (Big-O, как устроены dict и set).
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
