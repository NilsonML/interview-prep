"""LRU-кеш (LeetCode 146): хеш-таблица + двусвязный список.     [обязательно · неделя 4]

ИНТУИЦИЯ
    Стопка недавно открытых файлов: открыл файл — он наверху. Места нет — выкидываем
    самый нижний (least recently used — давно не использованный).

КАК УСТРОЕНО: две структуры работают вместе
    dict:  key -> узел списка                       (найти за O(1))
    список: HEAD <-> [k1] <-> [k3] <-> [k2] <-> TAIL  (переставить за O(1))
            старые                        свежие

    get(k1):  нашли узел через dict, вырезали из середины (O(1): у узла есть prev и next),
              вставили перед TAIL — теперь он самый свежий.
    put при переполнении: удаляем HEAD.next (самый старый) из списка И из dict —
              поэтому узел хранит свой key.
    HEAD и TAIL — фиктивные узлы (сторожа): список никогда не пуст, вставка и удаление
    без проверок на None.

ТЕРМИНЫ: политика вытеснения (LRU, LFU, FIFO), двусвязный список, сторожевой узел.
В Python есть готовые OrderedDict.move_to_end и functools.lru_cache — на интервью
их часто запрещают, поэтому полезно уметь без них.

ЗАДАНИЕ: без OrderedDict (dict использовать можно)
    - get(key) -> значение или -1, ключ становится самым свежим;
    - put(key, value): вставка или обновление (тоже делает свежим); при переполнении
      удаляется самый старый;
    - обе операции O(1); __len__.
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
