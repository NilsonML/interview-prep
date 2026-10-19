"""Метрики классификации и регрессии с нуля (только NumPy).     [неделя 5]

На ML-интервью просят посчитать метрику руками и объяснить, когда она врёт.
Тесты сверяют твою реализацию с sklearn.

ИНТУИЦИЯ
    Precision — «когда модель кричит "мошенник", как часто права?»
    Recall    — «какую долю мошенников модель вообще заметила?»
    ROC-AUC   — турнир: берём случайного мошенника и случайного честного клиента;
                AUC = вероятность, что модель поставит мошеннику скор выше.
                Не зависит от порога и от масштаба скоров — только от порядка.
    Log loss  — штраф за уверенность в неправильном ответе: предсказал 0.99,
                а было 0 -> огромный штраф.

ВЕКТОРИЗАЦИЯ: никаких циклов по объектам там, где можно (y_true == 1) & (y_pred == 1).
"""

import numpy as np


def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """Матрица ошибок для бинарной задачи: [[TN, FP], [FN, TP]] (строки — истина).

    >>> confusion_matrix(np.array([0, 1, 1, 0]), np.array([0, 1, 0, 1]))
    array([[1, 1],
           [1, 1]])
    """
    raise NotImplementedError


def precision_recall_f1(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float, float]:
    """Precision, recall и F1 для класса 1. Деление на 0 -> метрика 0.0.

    Подумай: почему accuracy 99% бесполезна при 1% положительного класса?
    """
    raise NotImplementedError


def roc_auc(y_true: np.ndarray, scores: np.ndarray) -> float:
    """ROC-AUC = вероятность, что случайный положительный пример получит скор выше
    случайного отрицательного (ничьи считаются за 1/2).

    Цель: O(n log n) через ранги (статистика Манна — Уитни), а не O(n^2) по всем парам.
    Без sklearn.
    """
    raise NotImplementedError


def log_loss(y_true: np.ndarray, proba: np.ndarray, eps: float = 1e-15) -> float:
    """Бинарная кросс-энтропия: -mean(y log p + (1-y) log(1-p)).
    Вероятности обрезай в [eps, 1-eps], иначе log(0) = -inf.
    """
    raise NotImplementedError


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Коэффициент детерминации: 1 - SS_res / SS_tot.
    1 — идеально, 0 — не лучше константы «среднее», < 0 — хуже константы.
    """
    raise NotImplementedError
