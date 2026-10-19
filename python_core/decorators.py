"""Замыкания и декораторы.     [неделя 2]

ЗАМЫКАНИЕ: функция, которая «унесла с собой» переменные места, где её создали.
Аналогия: рюкзак — внутренняя функция ушла из внешней, а переменные лежат у неё в рюкзаке.
    def make_adder(n):
        def add(x):
            return x + n      # n живёт в замыкании add
        return add

ДЕКОРАТОР: функция, которая принимает функцию и возвращает обёртку.
@decorator над def f — это ровно f = decorator(f). Аналогия: подарочная упаковка —
внутри та же функция, снаружи логирование, кеш, повторы, замер времени.

ПРАВИЛА
    - обёртку оформляй через @functools.wraps(func), иначе потеряются __name__ и __doc__
      (тесты это проверяют);
    - декоратор С ПАРАМЕТРАМИ — фабрика декораторов: retry(3) -> decorator -> wrapper,
      три уровня вложенности;
    - nonlocal нужен, чтобы ПРИСВОИТЬ переменной из замыкания (без него создастся локальная).
"""

import functools
import time
from collections.abc import Callable
from typing import Any


def make_counter() -> Callable[[], int]:
    """Замыкание: каждый вызов возвращает следующее число 1, 2, 3, ...
    У каждого счётчика своё состояние. Без глобальных переменных и классов.

    >>> c = make_counter()
    >>> c(), c()
    (1, 2)
    """
    count = 0

    def counter() -> int:
        nonlocal count  # без nonlocal присваивание создало бы новую локальную переменную
        count += 1
        return count

    return counter


def count_calls(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор: считает вызовы функции в атрибуте wrapper.calls."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор: записывает длительность последнего вызова в секундах в wrapper.last_elapsed.
    Время считай даже если функция бросила исключение."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:  # finally выполнится и при return, и при исключении
            wrapper.last_elapsed = time.perf_counter() - start

    wrapper.last_elapsed = None
    return wrapper


def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор: кеширует результат по позиционным аргументам (как functools.cache,
    но сам). Без functools.cache / lru_cache."""
    cache: dict[tuple[Any, ...], Any] = {}

    @functools.wraps(func)
    def wrapper(*args: Any) -> Any:
        if args not in cache:  # args — кортеж, он хешируем (если хешируемы элементы)
            cache[args] = func(*args)
        return cache[args]

    return wrapper


def retry(
    times: int, exceptions: tuple[type[BaseException], ...] = (Exception,), delay: float = 0.0
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор С ПАРАМЕТРАМИ: повторить вызов до times раз, если упало одно из exceptions;
    между попытками ждать delay секунд. После последней неудачи пробросить исключение.
    Другие исключения пробрасываются сразу.

    @retry(times=3, exceptions=(ConnectionError,))
    def fetch(): ...

    Подумай: почему здесь три уровня вложенных функций?
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise  # голый raise сохраняет исходный traceback
                    time.sleep(delay)
            return None  # недостижимо при times >= 1

        return wrapper

    return decorator
