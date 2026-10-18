"""Замыкания и декораторы.

Замыкание — вложенная функция, которая помнит переменные внешней функции.
Декоратор — функция, которая принимает функцию и возвращает новую (обёртку).
@decorator над def f — это просто f = decorator(f).

Правило: обёртку всегда оформляй через functools.wraps, иначе потеряются
__name__ и __doc__ исходной функции (это проверяют тесты).
"""

from collections.abc import Callable
from typing import Any


def make_counter() -> Callable[[], int]:
    """Замыкание: каждый вызов возвращает следующее число 1, 2, 3, ...
    У каждого счётчика своё состояние. Без глобальных переменных и классов.

    >>> c = make_counter()
    >>> c(), c()
    (1, 2)
    """
    raise NotImplementedError


def count_calls(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор: считает вызовы функции в атрибуте wrapper.calls."""
    raise NotImplementedError


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор: записывает длительность последнего вызова в секундах в wrapper.last_elapsed.
    Время считай даже если функция бросила исключение."""
    raise NotImplementedError


def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор: кеширует результат по позиционным аргументам (как functools.cache,
    но сам). Без functools.cache / lru_cache."""
    raise NotImplementedError


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
    raise NotImplementedError
