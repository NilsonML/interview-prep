"""Контекстные менеджеры (with).     [неделя 3]

ИНТУИЦИЯ: «взял — положи на место», даже если по дороге всё пошло не так.
with гарантирует закрывающее действие при любом исходе блока: закрыть файл,
отпустить лок, вернуть настройку, откатить транзакцию в БД.

КАК РАБОТАЕТ
    with mgr as x:        x = mgr.__enter__()
        body              try: body
                          finally: mgr.__exit__(тип, исключение, traceback)
    Если __exit__ вернул True, исключение из блока подавляется.

ДВА СПОСОБА НАПИСАТЬ СВОЙ
    1) класс с __enter__ / __exit__ — когда нужен объект с состоянием (Timer.elapsed);
    2) генератор с @contextlib.contextmanager: код до yield — вход, после yield
       (обязательно в finally) — выход.
"""

import time
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
        self.elapsed: float | None = None

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self  # то, что окажется после "as"

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        self.elapsed = time.perf_counter() - self._start
        return False  # True подавило бы исключение из блока


@contextmanager
def suppress(*exceptions: type[BaseException]) -> Iterator[None]:
    """Свой аналог contextlib.suppress: проглатывает перечисленные исключения.

    with suppress(KeyError):
        {}["missing"]       # программа идёт дальше
    """
    try:
        yield
    except exceptions:
        pass


@contextmanager
def temporary_attr(obj: Any, name: str, value: Any) -> Iterator[Any]:
    """Временно подменить атрибут объекта и обязательно вернуть старое значение
    (даже при исключении). Если атрибута не было — после блока его не должно быть.
    Так работает mock.patch в тестах.

    with temporary_attr(config, "DEBUG", True):
        ...
    """
    missing = object()  # уникальный маркер: отличает «атрибута нет» от «атрибут = None»
    old = getattr(obj, name, missing)
    setattr(obj, name, value)
    try:
        yield obj
    finally:
        if old is missing:
            delattr(obj, name)
        else:
            setattr(obj, name, old)
