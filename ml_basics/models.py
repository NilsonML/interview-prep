"""Классические модели с нуля на NumPy.     [недели 8–10]

Цель не в том, чтобы обогнать sklearn, а в том, чтобы уметь вывести и объяснить.
Интерфейс как у sklearn: fit(X, y) -> self, predict(X).

ИНТУИЦИЯ
    Градиентный спуск — спуск с горы в тумане: делаешь шаг туда, где круче всего вниз.
        lr слишком большой — перепрыгиваешь долину; слишком маленький — идёшь вечность.
    Логистическая регрессия — линейная модель + сигмоида, которая сжимает любое число в (0, 1).
        Градиент log loss удивительно простой: X^T (p - y) / n — «ошибка, взвешенная признаками».
    L2-регуляризация — «резинка», тянущая веса к нулю: модель не опирается сильно на один признак.
    kNN — «скажи мне, кто твои соседи». Обучения нет, вся работа при предсказании.
    k-means — центры кластеров переезжают в центр своих точек, пока не перестанут двигаться.
        Сходится к ЛОКАЛЬНОМУ минимуму, поэтому делают несколько запусков.

ВЕКТОРИЗАЦИЯ: попарные расстояния без циклов: ||a - b||^2 = ||a||^2 + ||b||^2 - 2 a·b.
"""

import numpy as np


class LinearRegression:
    """Линейная регрессия по методу наименьших квадратов.

    method="normal": аналитическое решение (X^T X)^-1 X^T y. Подсказка: np.linalg.lstsq
        устойчивее явного обращения матрицы.
    method="gd": градиентный спуск по MSE с шагом lr и n_iter итерациями.
        Градиент MSE по w: (2/n) X^T (Xw - y).
    Свободный член (intercept_) обучается отдельно от коэффициентов (coef_).
    """

    def __init__(self, method: str = "normal", lr: float = 0.1, n_iter: int = 2000) -> None:
        self.method, self.lr, self.n_iter = method, lr, n_iter

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LinearRegression":
        X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
        Xb = np.hstack([np.ones((len(X), 1)), X])  # столбец единиц = свободный член
        if self.method == "normal":
            w = np.linalg.lstsq(Xb, y, rcond=None)[0]
        elif self.method == "gd":
            w = np.zeros(Xb.shape[1])
            for _ in range(self.n_iter):
                grad = 2 / len(y) * Xb.T @ (Xb @ w - y)
                w -= self.lr * grad
        else:
            raise ValueError(f"unknown method {self.method!r}")
        self.intercept_, self.coef_ = w[0], w[1:]
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.asarray(X, dtype=float) @ self.coef_ + self.intercept_


def sigmoid(z: np.ndarray) -> np.ndarray:
    """1 / (1 + e^-z), устойчиво к переполнению при больших |z|."""
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1 / (1 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])  # для z < 0 считаем через e^z, чтобы не было exp(большого)
    out[~pos] = ez / (1 + ez)
    return out


class LogisticRegression:
    """Бинарная логистическая регрессия: градиентный спуск по log loss + L2-регуляризация.

    Градиент log loss по w: (1/n) X^T (sigmoid(Xw) - y) + l2 * w  (свободный член не
    регуляризуется). predict_proba(X) -> вероятности класса 1 (одномерный массив),
    predict(X) -> 0/1 по порогу 0.5.
    """

    def __init__(self, lr: float = 0.1, n_iter: int = 2000, l2: float = 0.0) -> None:
        self.lr, self.n_iter, self.l2 = lr, n_iter, l2

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LogisticRegression":
        X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
        self.coef_, self.intercept_ = np.zeros(X.shape[1]), 0.0
        for _ in range(self.n_iter):
            error = sigmoid(X @ self.coef_ + self.intercept_) - y  # производная log loss по логиту
            self.coef_ -= self.lr * (X.T @ error / len(y) + self.l2 * self.coef_)
            self.intercept_ -= self.lr * error.mean()
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return sigmoid(np.asarray(X, dtype=float) @ self.coef_ + self.intercept_)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return (self.predict_proba(X) >= 0.5).astype(int)


class KNNClassifier:
    """k ближайших соседей, евклидово расстояние, голосование большинством
    (при равенстве голосов — меньший класс). Векторизуй расстояния без циклов
    по парам: ||a - b||^2 = ||a||^2 + ||b||^2 - 2 a·b.
    """

    def __init__(self, k: int = 5) -> None:
        self.k = k

    def fit(self, X: np.ndarray, y: np.ndarray) -> "KNNClassifier":
        self.X_, self.y_ = np.asarray(X, dtype=float), np.asarray(y)  # «обучение» = запомнить
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        X = np.asarray(X, dtype=float)
        d2 = (X**2).sum(1)[:, None] + (self.X_**2).sum(1)[None, :] - 2 * X @ self.X_.T
        nearest = np.argsort(d2, axis=1, kind="stable")[:, : self.k]
        labels = self.y_[nearest]
        # bincount + argmax: argmax берёт первый максимум, то есть меньший класс при ничьей
        return np.array([np.bincount(row).argmax() for row in labels])


class KMeans:
    """k-means (алгоритм Ллойда) с несколькими случайными стартами.

    Один запуск: k случайных различных точек выборки как центры, затем повторять
    «назначить кластеры -> пересчитать центры» до сходимости или max_iter.
    Пустой кластер сохраняет старый центр.
    k-means сходится к ЛОКАЛЬНОМУ минимуму: два центра могут застрять в одном
    кластере. Поэтому делаем n_init запусков (генератор np.random.default_rng(seed)
    общий на все) и оставляем результат с наименьшей inertia_.
    Атрибуты после fit: cluster_centers_, labels_, inertia_ (сумма квадратов расстояний
    до своих центров).
    """

    def __init__(self, k: int, n_init: int = 10, max_iter: int = 100, seed: int = 0) -> None:
        self.k, self.n_init, self.max_iter, self.seed = k, n_init, max_iter, seed

    @staticmethod
    def _assign(X: np.ndarray, centers: np.ndarray) -> np.ndarray:
        d2 = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(-1)  # (n, k) квадраты расстояний
        return d2.argmin(axis=1)

    def _single_run(self, X: np.ndarray, rng: np.random.Generator) -> tuple[np.ndarray, float]:
        centers = X[rng.choice(len(X), self.k, replace=False)]
        for _ in range(self.max_iter):
            labels = self._assign(X, centers)
            new_centers = np.array(
                [
                    X[labels == j].mean(axis=0) if np.any(labels == j) else centers[j]
                    for j in range(self.k)
                ]
            )
            if np.allclose(new_centers, centers):
                break
            centers = new_centers
        inertia = float(((X - centers[self._assign(X, centers)]) ** 2).sum())
        return centers, inertia

    def fit(self, X: np.ndarray) -> "KMeans":
        X = np.asarray(X, dtype=float)
        rng = np.random.default_rng(self.seed)
        runs = [self._single_run(X, rng) for _ in range(self.n_init)]
        self.cluster_centers_, self.inertia_ = min(runs, key=lambda r: r[1])
        self.labels_ = self._assign(X, self.cluster_centers_)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self._assign(np.asarray(X, dtype=float), self.cluster_centers_)
