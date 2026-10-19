"""Тесты «предскажи результат»: твой ответ в ANSWERS сравнивается с настоящим.

Ответ ... (Ellipsis) означает «ещё не отвечал» — тест считается нерешённым.
"""

import warnings

import pytest

from predict import numpy_ml, python_basics, structures

CASES = [
    (module, key)
    for module in (python_basics, structures, numpy_ml)
    for key in sorted(module.ANSWERS)
]


@pytest.mark.parametrize(
    "module, key", CASES, ids=[f"{m.__name__.split('.')[-1]}-{k}" for m, k in CASES]
)
def test_prediction(module, key):
    answer = module.ANSWERS[key]
    if answer is ...:
        raise NotImplementedError
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # некоторые фрагменты намеренно «плохие»
        real = getattr(module, key)()
    assert answer == real, f"{key}: ты ответил {answer!r}, на самом деле {real!r}"
