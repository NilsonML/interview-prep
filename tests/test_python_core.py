"""Тесты: генераторы, итераторы, замыкания, декораторы, контекстные менеджеры, collections."""

import itertools
import time
import types

import pytest

from python_core import collections_tasks as ct
from python_core import context_managers as cm
from python_core import decorators as dec
from python_core import generators as gen

# ---------------------------------------------------------------- generators


def test_fibonacci_is_lazy_and_infinite():
    g = gen.fibonacci()
    assert isinstance(g, types.GeneratorType)
    assert list(itertools.islice(g, 10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_powers():
    assert list(gen.powers(2, 5)) == [1, 2, 4, 8, 16]
    assert list(gen.powers(3, 0)) == []
    assert isinstance(gen.powers(2, 3), types.GeneratorType)


def test_take():
    assert gen.take(gen.fibonacci(), 5) == [0, 1, 1, 2, 3]
    assert gen.take([1, 2], 5) == [1, 2]
    assert gen.take(gen.fibonacci(), 0) == []


def test_take_does_not_overconsume():
    it = iter(range(10))
    gen.take(it, 3)
    assert next(it) == 3  # взяли ровно 3 элемента, четвёртый остался в итераторе


def test_chunked_is_lazy():
    assert list(gen.chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert list(gen.chunked([], 3)) == []
    first = next(gen.chunked(itertools.count(), 3))  # работает на бесконечном входе
    assert first == [0, 1, 2]


def test_flatten():
    assert list(gen.flatten([1, [2, [3, [4, [5]]]], 6])) == [1, 2, 3, 4, 5, 6]
    assert list(gen.flatten(["ab", ["cd"]])) == ["ab", "cd"]
    assert list(gen.flatten([])) == []


def test_sliding_windows():
    assert list(gen.sliding_windows([1, 2, 3, 4], 3)) == [(1, 2, 3), (2, 3, 4)]
    assert list(gen.sliding_windows(iter(range(3)), 2)) == [(0, 1), (1, 2)]
    assert list(gen.sliding_windows([1], 2)) == []


def test_countdown_is_reusable_iterable():
    c = gen.Countdown(3)
    assert list(c) == [3, 2, 1]
    assert list(c) == [3, 2, 1]  # второй проход тоже работает
    it = iter(c)
    assert next(it) == 3 and iter(it) is it
    assert list(gen.Countdown(0)) == []


# ---------------------------------------------------------------- closures and decorators


def test_make_counter_independent_state():
    a, b = dec.make_counter(), dec.make_counter()
    assert [a(), a(), a()] == [1, 2, 3]
    assert b() == 1


def test_count_calls_preserves_metadata():
    @dec.count_calls
    def add(x, y=0):
        """Складывает."""
        return x + y

    assert add(1, y=2) == 3 and add(5) == 5
    assert add.calls == 2
    assert add.__name__ == "add" and add.__doc__ == "Складывает."  # functools.wraps


def test_timer():
    @dec.timer
    def slow():
        time.sleep(0.05)
        return "ok"

    assert slow() == "ok" and slow.last_elapsed >= 0.05

    @dec.timer
    def boom():
        raise ValueError

    with pytest.raises(ValueError):
        boom()
    assert boom.last_elapsed is not None  # время записано даже при исключении


def test_memoize():
    calls = []

    @dec.memoize
    def fib(n):
        calls.append(n)
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    assert fib(80) == 23416728348467685
    assert len(calls) == 81  # каждое n посчитано ровно один раз
    assert fib.__name__ == "fib"


def test_retry():
    attempts = []

    @dec.retry(times=3, exceptions=(ConnectionError,))
    def flaky():
        attempts.append(1)
        if len(attempts) < 3:
            raise ConnectionError
        return "ok"

    assert flaky() == "ok" and len(attempts) == 3

    @dec.retry(times=2, exceptions=(ConnectionError,))
    def always_fails():
        attempts.append(1)
        raise ConnectionError("down")

    attempts.clear()
    with pytest.raises(ConnectionError):
        always_fails()
    assert len(attempts) == 2

    @dec.retry(times=5, exceptions=(ConnectionError,))
    def wrong_error():
        attempts.append(1)
        raise KeyError

    attempts.clear()
    with pytest.raises(KeyError):
        wrong_error()
    assert len(attempts) == 1  # чужие исключения не ретраятся
    assert flaky.__name__ == "flaky"


# ---------------------------------------------------------------- context managers


def test_timer_context_manager():
    with cm.Timer() as t:
        time.sleep(0.02)
    assert t.elapsed >= 0.02

    t2 = cm.Timer()
    with pytest.raises(RuntimeError), t2:
        raise RuntimeError  # исключение не подавлено
    assert t2.elapsed is not None


def test_suppress():
    with cm.suppress(KeyError, IndexError):
        {}["missing"]
    with pytest.raises(ValueError), cm.suppress(KeyError):
        raise ValueError


def test_temporary_attr():
    obj = types.SimpleNamespace(debug=False)
    with cm.temporary_attr(obj, "debug", True):
        assert obj.debug is True
    assert obj.debug is False

    with pytest.raises(ZeroDivisionError), cm.temporary_attr(obj, "debug", True):
        raise ZeroDivisionError
    assert obj.debug is False  # восстановлено даже при исключении

    with cm.temporary_attr(obj, "new_attr", 1):
        assert obj.new_attr == 1
    assert not hasattr(obj, "new_attr")


# ---------------------------------------------------------------- collections


def test_first_unique_char():
    assert ct.first_unique_char("leetcode") == 0
    assert ct.first_unique_char("loveleetcode") == 2
    assert ct.first_unique_char("aabb") == -1


def test_group_by():
    assert ct.group_by(["apple", "avocado", "banana"], key=lambda w: w[0]) == {
        "a": ["apple", "avocado"],
        "b": ["banana"],
    }
    assert ct.group_by(range(6), key=lambda x: x % 2) == {0: [0, 2, 4], 1: [1, 3, 5]}


def test_merge_counts():
    assert ct.merge_counts({"a": 1, "b": 2}, {"b": 3, "c": 1}) == {"a": 1, "b": 5, "c": 1}
    assert ct.merge_counts() == {}


def test_most_common_words():
    assert ct.most_common_words("b a, A! b c a", 2) == [("a", 3), ("b", 2)]
    assert ct.most_common_words('Кот (кот) "кот"; пёс — пёс', 2) == [("кот", 3), ("пёс", 2)]


def test_sliding_window_max():
    assert ct.sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert ct.sliding_window_max([1], 1) == [1]
    assert ct.sliding_window_max([9, 8, 7, 6], 2) == [9, 8, 7]
