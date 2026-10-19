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
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    return np.array([[tn, fp], [fn, tp]])


def precision_recall_f1(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float, float]:
    """Precision, recall и F1 для класса 1. Деление на 0 -> метрика 0.0.

    Подумай: почему accuracy 99% бесполезна при 1% положительного класса?
    """
    (_, fp), (fn, tp) = confusion_matrix(y_true, y_pred)
    precision = tp / (tp + fp) if tp + fp else 0.0  # из предсказанных 1 — сколько верно
    recall = tp / (tp + fn) if tp + fn else 0.0  # из настоящих 1 — сколько нашли
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def roc_auc(y_true: np.ndarray, scores: np.ndarray) -> float:
    """ROC-AUC = вероятность, что случайный положительный пример получит скор выше
    случайного отрицательного (ничьи считаются за 1/2).

    Цель: O(n log n) через ранги (статистика Манна — Уитни), а не O(n^2) по всем парам.
    Без sklearn.
    """
    y_true, scores = np.asarray(y_true), np.asarray(scores, dtype=float)
    order = np.argsort(scores, kind="mergesort")
    sorted_scores = scores[order]
    ranks = np.empty(len(scores))
    i = 0
    while i < len(scores):  # равным скорам — средний ранг (так учитываются ничьи)
        j = i
        while j + 1 < len(scores) and sorted_scores[j + 1] == sorted_scores[i]:
            j += 1
        ranks[order[i : j + 1]] = (i + j) / 2 + 1  # ранги с 1
        i = j + 1
    n_pos = int(np.sum(y_true == 1))
    n_neg = len(y_true) - n_pos
    # Сумма рангов положительных минус минимально возможная = число «выигранных» пар
    return (ranks[y_true == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def log_loss(y_true: np.ndarray, proba: np.ndarray, eps: float = 1e-15) -> float:
    """Бинарная кросс-энтропия: -mean(y log p + (1-y) log(1-p)).
    Вероятности обрезай в [eps, 1-eps], иначе log(0) = -inf.
    """
    y_true = np.asarray(y_true, dtype=float)
    p = np.clip(np.asarray(proba, dtype=float), eps, 1 - eps)
    return float(-np.mean(y_true * np.log(p) + (1 - y_true) * np.log(1 - p)))


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Коэффициент детерминации: 1 - SS_res / SS_tot.
    1 — идеально, 0 — не лучше константы «среднее», < 0 — хуже константы.
    """
    y_true, y_pred = np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - y_true.mean()) ** 2)
    return float(1 - ss_res / ss_tot)
