"""Почини баг: ML и NumPy.     [недели 5–10]

Самые дорогие баги в ML не падают с исключением: код работает, метрика выглядит
прилично, а модель бесполезна или оценка завышена. Поэтому здесь тесты проверяют
свойства результата (нет пересечения train и test, средние нулевые, метрика конечна).

Порядок работы как в python_bugs.py: воспроизведи -> исправь минимально ->
комментарий «# БАГ: ... ИСПРАВЛЕНИЕ: ...» -> FIXED["имя"] = True -> pytest.
"""

import numpy as np

FIXED = {
    "standardize": False,
    "split_train_test": False,
    "scale_train_test": False,
    "precision": False,
    "log_loss": False,
    "sigmoid": False,
    "k_fold_indices": False,
    "evaluate": False,
}


def standardize(X: np.ndarray) -> np.ndarray:
    """Каждый ПРИЗНАК (столбец) -> среднее 0, стандартное отклонение 1.

    Жалоба: «После standardize у признаков средние не нулевые, а у каждой строки — нулевые».
    """
    return (X - X.mean(axis=1, keepdims=True)) / X.std(axis=1, keepdims=True)


def split_train_test(n: int, test_size: float, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Индексы train и test: не пересекаются и вместе покрывают 0..n-1.
    В test round(n * test_size) объектов.

    Жалоба: «Метрика на test подозрительно высокая; оказалось, часть объектов есть
    и в train, и в test».
    """
    rng = np.random.default_rng(seed)
    n_test = round(n * test_size)
    test = rng.choice(n, size=n_test, replace=True)
    train = rng.choice(n, size=n - n_test, replace=True)
    return train, test


def scale_train_test(X_train: np.ndarray, X_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Стандартизировать train и test статистиками, посчитанными ТОЛЬКО по train.

    Жалоба: «На кросс-валидации всё прекрасно, в проде хуже. Ревьюер написал: утечка».
    """
    X_all = np.vstack([X_train, X_test])
    mean, std = X_all.mean(axis=0), X_all.std(axis=0)
    return (X_train - mean) / std, (X_test - mean) / std


def precision(y_true: list[int], y_pred: list[int]) -> float:
    """Precision для класса 1; если модель не предсказала ни одной 1 — вернуть 0.0.

    Жалоба: «На осторожной модели падает ZeroDivisionError».
    """
    tp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == 0 and p == 1)
    return tp / (tp + fp)


def log_loss(y_true: np.ndarray, proba: np.ndarray) -> float:
    """Бинарная кросс-энтропия. Должна быть конечной даже при proba ровно 0 или 1.

    Жалоба: «Один уверенный неправильный ответ — и в логах обучения loss = inf».
    """
    return float(-np.mean(y_true * np.log(proba) + (1 - y_true) * np.log(1 - proba)))


def sigmoid(z: np.ndarray) -> np.ndarray:
    """1 / (1 + e^-z) для массива, без переполнения при больших |z|.

    Жалоба: «На больших отрицательных логитах сыплются RuntimeWarning: overflow in exp».
    """
    return 1 / (1 + np.exp(-z))


def k_fold_indices(n: int, k: int) -> list[np.ndarray]:
    """k блоков индексов валидации (без перемешивания): каждый индекс 0..n-1 ровно в одном
    блоке, размеры блоков отличаются не больше чем на 1.

    Жалоба: «При n = 10, k = 3 последний объект никогда не попадает в валидацию».
    """
    size = n // k
    return [np.arange(i * size, (i + 1) * size) for i in range(k)]


def evaluate(model, X_train, y_train, X_test, y_test) -> float:
    """Обучить модель на train и вернуть accuracy на TEST.

    Жалоба: «Accuracy всегда около 1.0, даже на случайных метках».
    """
    model.fit(X_train, y_train)
    return float((model.predict(X_train) == y_train).mean())
