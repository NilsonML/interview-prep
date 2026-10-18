"""LRU-кеш (LeetCode 146) на хеш-таблице + двусвязном списке.

Задание: реализуй кеш ёмкости capacity БЕЗ OrderedDict (dict использовать можно).

Требования:
    - get(key) -> значение или -1; ключ становится "самым свежим";
    - put(key, value): вставка или обновление (тоже делает ключ свежим);
      при переполнении удаляется давно не использованный ключ;
    - обе операции за O(1);
    - __len__.

Подумай до кода:
    - dict даёт O(1) поиск, но как за O(1) переставить элемент в "свежий" конец
      и удалить самый старый? Какую структуру держать параллельно со словарём?
    - Зачем фиктивные узлы head / tail ("сторожа")? Сколько if-ов они убирают?
"""

from typing import Any


class LRUCache:
    def __init__(self, capacity: int) -> None:
        raise NotImplementedError

    def get(self, key: Any) -> Any:
        raise NotImplementedError

    def put(self, key: Any, value: Any) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
