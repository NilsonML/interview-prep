"""Контекстные менеджеры (with).

with гарантирует, что «закрывающее» действие выполнится, даже если внутри блока
произошло исключение: закрыть файл, отпустить лок, вернуть настройку, откатить транзакцию.

Два способа написать свой:
    1) класс с __enter__ / __exit__;
    2) генератор с @contextlib.contextmanager (код до yield — вход, после — выход).
"""

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any


class Timer:
    """Класс-контекстный менеджер: замеряет время блока.

    with Timer() as t:
        do_work()
    print(t.elapsed)   # секунды; заполняется и при исключении внутри блока

    Исключения из блока НЕ подавлять.
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def __enter__(self) -> "Timer":
        raise NotImplementedError

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        raise NotImplementedError


@contextmanager
def suppress(*exceptions: type[BaseException]) -> Iterator[None]:
    """Свой аналог contextlib.suppress: проглатывает перечисленные исключения.

    with suppress(KeyError):
        {}["missing"]       # программа идёт дальше
    """
    raise NotImplementedError


@contextmanager
def temporary_attr(obj: Any, name: str, value: Any) -> Iterator[Any]:
    """Временно подменить атрибут объекта и обязательно вернуть старое значение
    (даже при исключении). Если атрибута не было — после блока его не должно быть.
    Так работает mock.patch в тестах.

    with temporary_attr(config, "DEBUG", True):
        ...
    """
    raise NotImplementedError
