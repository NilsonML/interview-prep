"""Предскажи результат: NumPy и ML-ловушки.     [недели 5–10]

Большинство тихих багов в ML — это неверная ось, неожиданный broadcasting,
вид (view) вместо копии или метрика, которая «врёт» на несбалансированных данных.
Порядок работы как в python_basics.py.
"""

import numpy as np


def q01():
    """Форма результата broadcasting."""
    return (np.ones((3, 1)) + np.ones(4)).shape


def q02():
    """Сумма по оси 0."""
    return np.array([[1, 2], [3, 4]]).sum(axis=0).tolist()


def q03():
    """Среднее без указания оси."""
    return float(np.mean([[1, 2], [3, 4]]))


def q04():
    """Запись float в целочисленный массив."""
    a = np.array([1, 2, 3])
    a[0] = 2.7
    return a.tolist()


def q05():
    """Срез — вид (view) или копия?"""
    a = np.arange(5)
    b = a[1:3]
    b[0] = 99
    return a.tolist()


def q06():
    """Индексация списком — вид или копия?"""
    a = np.arange(5)
    c = a[[1, 2]]
    c[0] = -1
    return a.tolist()


def q07():
    """Формы X[:, 0] и X[:, [0]]."""
    X = np.zeros((3, 2))
    return X[:, 0].shape, X[:, [0]].shape


def q08():
    """argmax при равных значениях."""
    return int(np.argmax([1, 3, 3]))


def q09():
    """Точное сравнение float и isclose. Складываем по одному в цикле."""
    total = 0.0
    for _ in range(10):
        total += 0.1
    return bool(total == 1.0), bool(np.isclose(total, 1.0))


def q10():
    """Accuracy и recall модели «всегда 0» при 5% положительных."""
    y_true = np.array([0] * 95 + [1] * 5)
    y_pred = np.zeros(100, dtype=int)
    accuracy = float((y_true == y_pred).mean())
    recall = float(((y_true == 1) & (y_pred == 1)).sum() / (y_true == 1).sum())
    return accuracy, recall


def q11():
    """Log loss уверенного неправильного ответа против неуверенного."""

    def ll(y, p):
        return round(float(-(y * np.log(p) + (1 - y) * np.log(1 - p))), 2)

    return ll(1, 0.5), ll(1, 0.01)


def q12():
    """ROC-AUC не зависит от масштаба скоров: изменится ли порядок?"""
    scores = np.array([0.1, 0.4, 0.35, 0.8])
    transformed = np.log(scores) * 100 + 7
    return np.argsort(scores).tolist() == np.argsort(transformed).tolist()


ANSWERS = {
    "q01": (3, 4),  # (3,1) и (4,) -> (1,4) -> растягиваются до (3,4)
    "q02": [4, 6],  # axis=0 «схлопывает» строки: суммы по столбцам
    "q03": 2.5,  # без axis — среднее по всем элементам
    "q04": [2, 2, 3],  # dtype int: 2.7 молча обрезается до 2
    "q05": [0, 99, 2, 3, 4],  # срез — вид на те же данные
    "q06": [0, 1, 2, 3, 4],  # «необычная» индексация списком создаёт копию
    "q07": ((3,), (3, 1)),  # скаляр-индекс убирает ось, список — сохраняет
    "q08": 1,  # argmax возвращает ПЕРВЫЙ максимум
    "q09": (False, True),  # 0.1 неточно в двоичном float: total = 0.9999999999999999.
    # (встроенный sum() с Python 3.12 компенсирует ошибку и дал бы ровно 1.0)
    "q10": (0.95, 0.0),  # 95% accuracy и ни одного найденного положительного
    "q11": (0.69, 4.61),  # -ln 0.5 = 0.69; -ln 0.01 = 4.61: уверенная ошибка дорогая
    "q12": True,  # монотонное преобразование не меняет порядок -> AUC тот же
}
