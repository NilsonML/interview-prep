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


class _Node:
    __slots__ = ("key", "value", "prev", "next")  # экономия памяти: нет __dict__ у узлов

    def __init__(self, key: Any = None, value: Any = None) -> None:
        self.key, self.value = key, value
        self.prev: _Node | None = None
        self.next: _Node | None = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._map: dict[Any, _Node] = {}
        # Сторожа: head.next — самый старый, tail.prev — самый свежий.
        # Список никогда не пуст, поэтому вставка/удаление без проверок на None.
        self._head, self._tail = _Node(), _Node()
        self._head.next, self._tail.prev = self._tail, self._head

    def _unlink(self, node: _Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _append(self, node: _Node) -> None:
        last = self._tail.prev
        last.next = node
        node.prev, node.next = last, self._tail
        self._tail.prev = node

    def get(self, key: Any) -> Any:
        node = self._map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._append(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._append(node)
            return
        if len(self._map) == self.capacity:
            oldest = self._head.next
            self._unlink(oldest)
            del self._map[oldest.key]  # поэтому узел хранит и ключ, а не только значение
        node = _Node(key, value)
        self._map[key] = node
        self._append(node)

    def __len__(self) -> int:
        return len(self._map)
