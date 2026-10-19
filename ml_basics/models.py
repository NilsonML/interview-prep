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
        raise NotImplementedError

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LinearRegression":
        raise NotImplementedError

    def predict(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError


def sigmoid(z: np.ndarray) -> np.ndarray:
    """1 / (1 + e^-z), устойчиво к переполнению при больших |z|."""
    raise NotImplementedError


class LogisticRegression:
    """Бинарная логистическая регрессия: градиентный спуск по log loss + L2-регуляризация.

    Градиент log loss по w: (1/n) X^T (sigmoid(Xw) - y) + l2 * w  (свободный член не
    регуляризуется). predict_proba(X) -> вероятности класса 1 (одномерный массив),
    predict(X) -> 0/1 по порогу 0.5.
    """

    def __init__(self, lr: float = 0.1, n_iter: int = 2000, l2: float = 0.0) -> None:
        raise NotImplementedError

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LogisticRegression":
        raise NotImplementedError

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def predict(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class KNNClassifier:
    """k ближайших соседей, евклидово расстояние, голосование большинством
    (при равенстве голосов — меньший класс). Векторизуй расстояния без циклов
    по парам: ||a - b||^2 = ||a||^2 + ||b||^2 - 2 a·b.
    """

    def __init__(self, k: int = 5) -> None:
        raise NotImplementedError

    def fit(self, X: np.ndarray, y: np.ndarray) -> "KNNClassifier":
        raise NotImplementedError

    def predict(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError


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
        raise NotImplementedError

    def fit(self, X: np.ndarray) -> "KMeans":
        raise NotImplementedError

    def predict(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError
