"""Разбиение данных и предобработка с нуля.

Главная тема — утечки данных: всё, что «учится» на данных (средние, std, пороги),
считается только на train и потом применяется к test.
"""

import numpy as np


def train_test_split(
    X: np.ndarray, y: np.ndarray, test_size: float = 0.2, seed: int = 0, stratify: bool = False
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Случайное разбиение. stratify=True — доля каждого класса в test такая же, как в y
    (в test от каждого класса round(n_class * test_size) объектов).
    Возвращает X_train, X_test, y_train, y_test. Генератор: np.random.default_rng(seed).
    """
    raise NotImplementedError


def k_fold_indices(n: int, k: int, seed: int = 0) -> list[tuple[np.ndarray, np.ndarray]]:
    """k-fold: список пар (train_idx, val_idx). Каждый объект ровно один раз в валидации,
    размеры фолдов отличаются не больше чем на 1. Индексы перемешаны генератором с seed.
    """
    raise NotImplementedError


class StandardScaler:
    """(x - mean) / std по столбцам. fit запоминает статистики, transform их применяет.
    Столбец с std = 0 не делить (оставить std = 1), иначе получится nan.
    """

    def fit(self, X: np.ndarray) -> "StandardScaler":
        raise NotImplementedError

    def transform(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError


def one_hot(labels: np.ndarray, n_classes: int | None = None) -> np.ndarray:
    """[0, 2, 1] -> матрица (3, 3) из нулей и единиц. n_classes по умолчанию max + 1.
    Без циклов по элементам: используй индексацию NumPy.
    """
    raise NotImplementedError
