"""Почини баг: ML и NumPy.     [недели 5–10]

Самые дорогие баги в ML не падают с исключением: код работает, метрика выглядит
прилично, а модель бесполезна или оценка завышена. Поэтому здесь тесты проверяют
свойства результата (нет пересечения train и test, средние нулевые, метрика конечна).

Порядок работы как в python_bugs.py: воспроизведи -> исправь минимально ->
комментарий «# БАГ: ... ИСПРАВЛЕНИЕ: ...» -> FIXED["имя"] = True -> pytest.
"""

import numpy as np

FIXED = {
    "standardize": True,
    "split_train_test": True,
    "scale_train_test": True,
    "precision": True,
    "log_loss": True,
    "sigmoid": True,
    "k_fold_indices": True,
    "evaluate": True,
}


def standardize(X: np.ndarray) -> np.ndarray:
    """Каждый ПРИЗНАК (столбец) -> среднее 0, стандартное отклонение 1.

    Жалоба: «После standardize у признаков средние не нулевые, а у каждой строки — нулевые».
    """
    # БАГ: axis=1 считал статистики по строкам (по объектам), а не по признакам.
    # ИСПРАВЛЕНИЕ: axis=0 — «вдоль объектов», результат на каждый столбец.
    return (X - X.mean(axis=0)) / X.std(axis=0)


def split_train_test(n: int, test_size: float, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Индексы train и test: не пересекаются и вместе покрывают 0..n-1.
    В test round(n * test_size) объектов.

    Жалоба: «Метрика на test подозрительно высокая; оказалось, часть объектов есть
    и в train, и в test».
    """
    # БАГ: два независимых выбора с возвращением — повторы внутри и пересечение между частями.
    # ИСПРАВЛЕНИЕ: одна перестановка, разрезанная на две части.
    rng = np.random.default_rng(seed)
    n_test = round(n * test_size)
    perm = rng.permutation(n)
    return perm[n_test:], perm[:n_test]


def scale_train_test(X_train: np.ndarray, X_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Стандартизировать train и test статистиками, посчитанными ТОЛЬКО по train.

    Жалоба: «На кросс-валидации всё прекрасно, в проде хуже. Ревьюер написал: утечка».
    """
    # БАГ: среднее и std считались по train + test — статистики test утекали в обучение.
    # ИСПРАВЛЕНИЕ: fit только на train, transform для обоих.
    mean, std = X_train.mean(axis=0), X_train.std(axis=0)
    return (X_train - mean) / std, (X_test - mean) / std


def precision(y_true: list[int], y_pred: list[int]) -> float:
    """Precision для класса 1; если модель не предсказала ни одной 1 — вернуть 0.0.

    Жалоба: «На осторожной модели падает ZeroDivisionError».
    """
    tp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == 0 and p == 1)
    # БАГ: при tp + fp == 0 делили на ноль.
    # ИСПРАВЛЕНИЕ: явно обрабатываем случай «нет положительных предсказаний» (как sklearn).
    return tp / (tp + fp) if tp + fp else 0.0


def log_loss(y_true: np.ndarray, proba: np.ndarray) -> float:
    """Бинарная кросс-энтропия. Должна быть конечной даже при proba ровно 0 или 1.

    Жалоба: «Один уверенный неправильный ответ — и в логах обучения loss = inf».
    """
    # БАГ: log(0) = -inf.
    # ИСПРАВЛЕНИЕ: обрезаем вероятности в [eps, 1 - eps].
    eps = 1e-15
    p = np.clip(proba, eps, 1 - eps)
    return float(-np.mean(y_true * np.log(p) + (1 - y_true) * np.log(1 - p)))


def sigmoid(z: np.ndarray) -> np.ndarray:
    """1 / (1 + e^-z) для массива, без переполнения при больших |z|.

    Жалоба: «На больших отрицательных логитах сыплются RuntimeWarning: overflow in exp».
    """
    # БАГ: при z = -1000 считали exp(1000) — переполнение float64.
    # ИСПРАВЛЕНИЕ: две ветки; для z < 0 считаем через e^z, он всегда <= 1.
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1 / (1 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1 + ez)
    return out


def k_fold_indices(n: int, k: int) -> list[np.ndarray]:
    """k блоков индексов валидации (без перемешивания): каждый индекс 0..n-1 ровно в одном
    блоке, размеры блоков отличаются не больше чем на 1.

    Жалоба: «При n = 10, k = 3 последний объект никогда не попадает в валидацию».
    """
    # БАГ: n // k терял остаток n % k.
    # ИСПРАВЛЕНИЕ: array_split раздаёт остаток по одному в первые блоки.
    return np.array_split(np.arange(n), k)


def evaluate(model, X_train, y_train, X_test, y_test) -> float:
    """Обучить модель на train и вернуть accuracy на TEST.

    Жалоба: «Accuracy всегда около 1.0, даже на случайных метках».
    """
    model.fit(X_train, y_train)
    # БАГ: качество мерили на обучающих данных — модель, запомнившая train, получала ~1.0.
    # ИСПРАВЛЕНИЕ: предсказываем и сравниваем на отложенной выборке.
    return float((model.predict(X_test) == y_test).mean())
