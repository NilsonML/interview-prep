"""Тесты структур данных. Проверяют только публичный интерфейс из docstring модулей."""

import random

import pytest

from data_structures.bst import BST
from data_structures.dynamic_array import DynamicArray
from data_structures.hash_map import HashMap
from data_structures.heap import MinHeap
from data_structures.linked_list import LinkedList
from data_structures.lru_cache import LRUCache
from data_structures.stack_queue import MinStack, QueueFromStacks, RingBuffer
from data_structures.trie import Trie
from data_structures.union_find import UnionFind

# ---------------------------------------------------------------- HashMap


class BadKey:
    """Все ключи с одинаковым хешем: худший случай, всё в одной корзине."""

    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return 42

    def __eq__(self, other):
        return isinstance(other, BadKey) and other.v == self.v


def test_hash_map_basic():
    m = HashMap()
    m.put("a", 1)
    m.put("b", 2)
    m.put("a", 10)  # обновление не увеличивает размер
    assert m.get("a") == 10 and m.get("b") == 2 and len(m) == 2
    assert m.get("missing") is None and m.get("missing", 0) == 0
    m.remove("a")
    assert "a" not in m and "b" in m and len(m) == 1
    with pytest.raises(KeyError):
        m.remove("a")


def test_hash_map_resize_and_iter():
    m = HashMap(capacity=8)
    for i in range(10_000):
        m.put(i, i * i)
    assert len(m) == 10_000 and m.capacity >= 10_000 / 0.75
    assert all(m.get(i) == i * i for i in range(10_000))
    assert sorted(m) == list(range(10_000))


def test_hash_map_collisions_and_mixed_keys():
    m = HashMap()
    for i in range(50):
        m.put(BadKey(i), i)
    assert m.get(BadKey(17)) == 17
    m.remove(BadKey(17))
    assert BadKey(17) not in m and BadKey(18) in m and len(m) == 49
    m.put(1, "int")
    m.put("1", "str")
    m.put((1,), "tuple")
    assert (m.get(1), m.get("1"), m.get((1,))) == ("int", "str", "tuple")


def test_hash_map_matches_dict_randomized():
    rng = random.Random(0)
    m, d = HashMap(), {}
    for _ in range(5_000):
        key = rng.randrange(200)
        if rng.random() < 0.3 and key in d:
            m.remove(key)
            del d[key]
        else:
            m.put(key, rng.random())
            d[key] = m.get(key)
    assert len(m) == len(d) and sorted(m) == sorted(d)


# ---------------------------------------------------------------- DynamicArray


def test_dynamic_array():
    a = DynamicArray(capacity=1)
    for i in range(100):
        a.append(i)
    assert len(a) == 100 and a[0] == 0 and a[-1] == 99 and a.capacity >= 100
    a[5] = "x"
    assert a[5] == "x"
    a.insert(0, "first")
    a.insert(len(a), "last")
    assert a[0] == "first" and a[-1] == "last" and a[1] == 0
    assert a.pop() == "last" and len(a) == 101
    assert list(a)[:3] == ["first", 0, 1]
    with pytest.raises(IndexError):
        a[101]
    with pytest.raises(IndexError):
        a[-102]
    with pytest.raises(IndexError):
        DynamicArray().pop()


def test_dynamic_array_grows_geometrically():
    a = DynamicArray(capacity=1)
    resizes, last = 0, a.capacity
    for i in range(1_000):
        a.append(i)
        if a.capacity != last:
            resizes, last = resizes + 1, a.capacity
    assert resizes <= 20  # при росте на +константу было бы сотни перевыделений


# ---------------------------------------------------------------- LinkedList


def test_linked_list():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.pop_front()
    for x in [2, 3]:
        ll.push_back(x)
    ll.push_front(1)
    assert list(ll) == [1, 2, 3] and len(ll) == 3
    assert ll.find(2) and not ll.find(5)
    ll.reverse()
    assert list(ll) == [3, 2, 1]
    ll.push_back(0)  # tail после reverse должен быть корректным
    assert list(ll) == [3, 2, 1, 0]
    assert [ll.pop_front() for _ in range(4)] == [3, 2, 1, 0] and len(ll) == 0
    ll.push_back(7)  # после опустошения tail тоже должен сброситься
    assert list(ll) == [7]


# ---------------------------------------------------------------- Stacks and queues


def test_min_stack():
    s = MinStack()
    for x in [5, 3, 7, 3, 1]:
        s.push(x)
    assert s.get_min() == 1 and s.top() == 1
    s.pop()
    assert s.get_min() == 3
    s.pop()
    assert s.get_min() == 3  # второй 3 ещё в стеке
    s.pop()
    s.pop()
    assert s.get_min() == 5
    s.pop()
    for op in (s.pop, s.top, s.get_min):
        with pytest.raises(IndexError):
            op()


def test_queue_from_stacks():
    q = QueueFromStacks()
    q.enqueue(1)
    q.enqueue(2)
    assert q.dequeue() == 1
    q.enqueue(3)
    assert q.peek() == 2 and len(q) == 2
    assert [q.dequeue(), q.dequeue()] == [2, 3]
    with pytest.raises(IndexError):
        q.dequeue()


def test_ring_buffer():
    rb = RingBuffer(3)
    for x in [1, 2, 3]:
        rb.enqueue(x)
    with pytest.raises(OverflowError):
        rb.enqueue(4)
    assert rb.dequeue() == 1
    rb.enqueue(4)  # индекс "заворачивается" в начало массива
    assert [rb.dequeue() for _ in range(3)] == [2, 3, 4] and len(rb) == 0
    with pytest.raises(IndexError):
        rb.dequeue()


# ---------------------------------------------------------------- Heap


def test_min_heap_sorts():
    rng = random.Random(1)
    data = [rng.randint(-100, 100) for _ in range(500)]
    h = MinHeap()
    for x in data:
        h.push(x)
    assert h.peek() == min(data) and len(h) == 500
    assert [h.pop() for _ in range(500)] == sorted(data)
    with pytest.raises(IndexError):
        h.pop()


def test_heapify():
    data = [9, 4, 7, 1, 8, 2, 2, 6]
    h = MinHeap.heapify(data)
    assert data == [9, 4, 7, 1, 8, 2, 2, 6]  # вход не изменён
    assert [h.pop() for _ in range(len(data))] == sorted(data)


# ---------------------------------------------------------------- BST


def test_bst():
    t = BST()
    with pytest.raises(ValueError):
        t.min()
    assert t.height() == 0
    for x in [50, 30, 70, 20, 40, 60, 80, 30]:
        t.insert(x)
    assert len(t) == 7 and t.inorder() == [20, 30, 40, 50, 60, 70, 80]
    assert t.min() == 20 and t.max() == 80 and t.height() == 3
    assert 40 in t and 45 not in t
    t.remove(20)  # лист
    t.remove(70)  # два ребёнка
    t.remove(50)  # корень
    assert t.inorder() == [30, 40, 60, 80] and len(t) == 4
    with pytest.raises(KeyError):
        t.remove(999)


def test_bst_degenerate_height():
    t = BST()
    for x in range(100):
        t.insert(x)
    assert t.height() == 100  # отсортированная вставка вырождает дерево в список


def test_bst_randomized():
    rng = random.Random(2)
    t, ref = BST(), set()
    for _ in range(2_000):
        x = rng.randrange(300)
        if x in ref and rng.random() < 0.5:
            t.remove(x)
            ref.remove(x)
        else:
            t.insert(x)
            ref.add(x)
    assert t.inorder() == sorted(ref) and len(t) == len(ref)


# ---------------------------------------------------------------- Trie


def test_trie():
    t = Trie()
    for w in ["apple", "app", "apply", "banana", "band"]:
        t.insert(w)
    assert t.search("app") and t.search("apple") and not t.search("appl")
    assert t.starts_with("appl") and t.starts_with("ban") and not t.starts_with("c")
    assert t.words_with_prefix("app") == ["app", "apple", "apply"]
    assert t.words_with_prefix("ban") == ["banana", "band"]
    assert t.words_with_prefix("x") == []


# ---------------------------------------------------------------- UnionFind


def test_union_find():
    uf = UnionFind(6)
    assert uf.count == 6
    assert uf.union(0, 1) and uf.union(1, 2) and uf.union(3, 4)
    assert not uf.union(0, 2)  # уже в одном множестве
    assert uf.connected(0, 2) and not uf.connected(0, 3)
    assert uf.count == 3


# ---------------------------------------------------------------- LRU


def test_lru_cache():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1  # 1 стал свежим
    c.put(3, 3)  # вытесняет 2
    assert c.get(2) == -1
    c.put(1, 10)  # обновление делает 1 свежим
    c.put(4, 4)  # вытесняет 3
    assert c.get(3) == -1 and c.get(1) == 10 and c.get(4) == 4 and len(c) == 2
