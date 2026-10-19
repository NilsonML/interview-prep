"""Разбиение данных и предобработка с нуля.     [неделя 6]

ГЛАВНАЯ ТЕМА — утечка данных (data leakage). Всё, что «учится» на данных (средние,
std, пороги, словари категорий), считается ТОЛЬКО на train и потом применяется к test.
Аналогия: нельзя готовиться к экзамену по билетам, которые на нём попадутся, —
оценка будет завышена.

ПРИЁМЫ
    - стратификация: доля классов в test такая же, как во всех данных;
    - k-fold: каждый объект ровно раз в валидации -> оценка со средним и разбросом;
    - fit / transform: fit запоминает статистики, transform только применяет.
"""

import numpy as np


def train_test_split(
    X: np.ndarray, y: np.ndarray, test_size: float = 0.2, seed: int = 0, stratify: bool = False
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Случайное разбиение. stratify=True — доля каждого класса в test такая же, как в y
    (в test от каждого класса round(n_class * test_size) объектов).
    Возвращает X_train, X_test, y_train, y_test. Генератор: np.random.default_rng(seed).
    """
    X, y = np.asarray(X), np.asarray(y)
    rng = np.random.default_rng(seed)
    if stratify:
        test_idx = []
        for cls in np.unique(y):
            idx = rng.permutation(np.flatnonzero(y == cls))
            test_idx.extend(idx[: round(len(idx) * test_size)])
        test_mask = np.zeros(len(y), dtype=bool)
        test_mask[test_idx] = True
    else:
        perm = rng.permutation(len(y))
        test_mask = np.zeros(len(y), dtype=bool)
        test_mask[perm[: round(len(y) * test_size)]] = True
    return X[~test_mask], X[test_mask], y[~test_mask], y[test_mask]


def k_fold_indices(n: int, k: int, seed: int = 0) -> list[tuple[np.ndarray, np.ndarray]]:
    """k-fold: список пар (train_idx, val_idx). Каждый объект ровно один раз в валидации,
    размеры фолдов отличаются не больше чем на 1. Индексы перемешаны генератором с seed.
    """
    perm = np.random.default_rng(seed).permutation(n)
    folds = np.array_split(perm, k)  # array_split допускает неравные части
    return [
        (np.concatenate([f for j, f in enumerate(folds) if j != i]), folds[i]) for i in range(k)
    ]


class StandardScaler:
    """(x - mean) / std по столбцам. fit запоминает статистики, transform их применяет.
    Столбец с std = 0 не делить (оставить std = 1), иначе получится nan.
    """

    def fit(self, X: np.ndarray) -> "StandardScaler":
        X = np.asarray(X, dtype=float)
        self.mean_ = X.mean(axis=0)
        std = X.std(axis=0)
        self.scale_ = np.where(std == 0, 1.0, std)
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        return (np.asarray(X, dtype=float) - self.mean_) / self.scale_

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)


def one_hot(labels: np.ndarray, n_classes: int | None = None) -> np.ndarray:
    """[0, 2, 1] -> матрица (3, 3) из нулей и единиц. n_classes по умолчанию max + 1.
    Без циклов по элементам: используй индексацию NumPy.
    """
    labels = np.asarray(labels)
    n_classes = int(labels.max()) + 1 if n_classes is None else n_classes
    result = np.zeros((len(labels), n_classes))
    result[np.arange(len(labels)), labels] = 1  # «необычная» индексация: пары (строка, столбец)
    return result
