"""Тесты «почини баг». Пока FIXED[name] = False, задача считается нерешённой."""

import numpy as np
import pytest

from bugfix import algorithm_bugs as ab
from bugfix import ml_bugs as mb
from bugfix import python_bugs as pb


def require_fixed(module, name):
    if not module.FIXED[name]:
        raise NotImplementedError


# ---------------------------------------------------------------- Python


def test_add_tag():
    require_fixed(pb, "add_tag")
    assert pb.add_tag("a") == ["a"]
    assert pb.add_tag("b") == ["b"]
    mine = ["x"]
    assert pb.add_tag("y", mine) == ["x", "y"] and mine == ["x", "y"]


def test_make_multipliers():
    require_fixed(pb, "make_multipliers")
    assert [m(2) for m in pb.make_multipliers()] == [0, 2, 4, 6]


def test_remove_negatives():
    require_fixed(pb, "remove_negatives")
    data = [-1, -2, 3, -4, 5]
    assert pb.remove_negatives(data) == [3, 5]
    assert data == [-1, -2, 3, -4, 5]


def test_merge_config():
    require_fixed(pb, "merge_config")
    default = {"db": {"host": "localhost", "port": 5432}, "debug": False}
    merged = pb.merge_config(default, {"db": {"host": "prod"}, "debug": True})
    assert merged == {"db": {"host": "prod", "port": 5432}, "debug": True}
    assert default == {"db": {"host": "localhost", "port": 5432}, "debug": False}


def test_logged():
    require_fixed(pb, "logged")

    @pb.logged
    def greet(name):
        """Здоровается."""
        return f"hi {name}"

    assert greet("bob") == "hi bob" and pb.CALL_LOG[-1] == "greet"
    assert greet.__name__ == "greet" and greet.__doc__ == "Здоровается."


def test_mean_and_max():
    require_fixed(pb, "mean_and_max")
    assert pb.mean_and_max([1, 2, 6]) == (3, 6)
    assert pb.mean_and_max(x for x in [1, 2, 6]) == (3, 6)


def test_group_by_first_letter():
    require_fixed(pb, "group_by_first_letter")
    assert pb.group_by_first_letter(["apple", "banana", "avocado"]) == {
        "a": ["apple", "avocado"],
        "b": ["banana"],
    }


# ---------------------------------------------------------------- Algorithms


def test_binary_search():
    require_fixed(ab, "binary_search")
    nums = [1, 3, 5]
    assert [ab.binary_search(nums, t) for t in (0, 1, 3, 5, 7)] == [-1, 0, 1, 2, -1]
    assert ab.binary_search([], 1) == -1


def test_two_sum():
    require_fixed(ab, "two_sum")
    assert ab.two_sum([3, 2, 4], 6) == (1, 2)
    assert ab.two_sum([3, 3], 6) == (0, 1)


def test_max_profit():
    require_fixed(ab, "max_profit")
    assert ab.max_profit([7, 5, 6]) == 1
    assert ab.max_profit([7, 1, 5, 3, 6, 4]) == 5
    assert ab.max_profit([5, 4, 3]) == 0


def test_is_valid_brackets():
    require_fixed(ab, "is_valid_brackets")
    assert ab.is_valid_brackets("([]{})") and ab.is_valid_brackets("")
    assert not ab.is_valid_brackets("((") and not ab.is_valid_brackets("(]")


def test_merge_intervals():
    require_fixed(ab, "merge_intervals")
    data = [[5, 6], [1, 2]]
    assert ab.merge_intervals(data) == [[1, 2], [5, 6]] and data == [[5, 6], [1, 2]]
    assert ab.merge_intervals([[1, 10], [2, 3]]) == [[1, 10]]
    assert ab.merge_intervals([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]


def test_longest_unique_substring():
    require_fixed(ab, "longest_unique_substring")
    assert ab.longest_unique_substring("abba") == 2
    assert ab.longest_unique_substring("abcabcbb") == 3
    assert ab.longest_unique_substring("") == 0


def test_count_islands():
    require_fixed(ab, "count_islands")
    grid = [["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]]
    assert ab.count_islands(grid) == 2
    assert grid == [["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]]


def test_coin_change():
    require_fixed(ab, "coin_change")
    assert ab.coin_change([1, 3, 4], 6) == 2
    assert ab.coin_change([1, 2, 5], 11) == 3
    assert ab.coin_change([2], 3) == -1


# ---------------------------------------------------------------- ML


def test_standardize():
    require_fixed(mb, "standardize")
    X = np.random.default_rng(0).normal(5, 3, size=(50, 4))
    Z = mb.standardize(X)
    assert np.allclose(Z.mean(axis=0), 0) and np.allclose(Z.std(axis=0), 1)


def test_split_train_test():
    require_fixed(mb, "split_train_test")
    train, test = mb.split_train_test(100, 0.2, seed=1)
    assert len(test) == 20 and len(train) == 80
    assert not set(train) & set(test)
    assert sorted([*train, *test]) == list(range(100))


def test_scale_train_test():
    require_fixed(mb, "scale_train_test")
    rng = np.random.default_rng(0)
    X_train, X_test = rng.normal(0, 1, (80, 3)), rng.normal(10, 1, (20, 3))
    train_scaled, test_scaled = mb.scale_train_test(X_train, X_test)
    assert np.allclose(train_scaled.mean(axis=0), 0)  # при утечке среднее train сместится
    assert np.allclose(test_scaled, (X_test - X_train.mean(0)) / X_train.std(0))


def test_precision():
    require_fixed(mb, "precision")
    assert mb.precision([1, 0, 1], [0, 0, 0]) == 0.0
    assert mb.precision([1, 0, 1, 0], [1, 1, 1, 0]) == pytest.approx(2 / 3)


def test_log_loss():
    require_fixed(mb, "log_loss")
    loss = mb.log_loss(np.array([1, 0]), np.array([0.0, 1.0]))
    assert np.isfinite(loss) and loss > 10
    assert mb.log_loss(np.array([1]), np.array([0.5])) == pytest.approx(np.log(2))


def test_sigmoid():
    require_fixed(mb, "sigmoid")
    with np.errstate(over="raise"):
        s = mb.sigmoid(np.array([-1000.0, 0.0, 1000.0]))
    assert np.allclose(s, [0.0, 0.5, 1.0])


def test_k_fold_indices():
    require_fixed(mb, "k_fold_indices")
    folds = mb.k_fold_indices(10, 3)
    assert len(folds) == 3
    assert sorted(np.concatenate(folds).tolist()) == list(range(10))
    sizes = [len(f) for f in folds]
    assert max(sizes) - min(sizes) <= 1


class Memorizer:
    """Модель, которая запоминает train и угадывает на всём остальном."""

    def fit(self, X, y):
        self.memory = {tuple(x): label for x, label in zip(X, y, strict=True)}
        return self

    def predict(self, X):
        return np.array([self.memory.get(tuple(x), 0) for x in X])


def test_evaluate():
    require_fixed(mb, "evaluate")
    rng = np.random.default_rng(0)
    X_train, y_train = rng.normal(size=(50, 2)), rng.integers(0, 2, 50)
    X_test, y_test = rng.normal(size=(50, 2)), np.ones(50, dtype=int)
    # На test модель всегда отвечает 0, а все метки 1 -> честная accuracy = 0
    assert mb.evaluate(Memorizer(), X_train, y_train, X_test, y_test) == 0.0
