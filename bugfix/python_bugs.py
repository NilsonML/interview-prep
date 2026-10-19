"""Почини баг: Python.     [недели 1–3]

КАК РАБОТАТЬ (как с баг-репортом в реальной команде)
    1. Прочитай «жалобу пользователя» в docstring функции и сам код.
    2. Сначала ВОСПРОИЗВЕДИ: найди вход, на котором функция ведёт себя неправильно
       (в терминале или маленьким тестом). Не правь код, пока не увидел баг своими глазами.
    3. Исправь минимальным изменением и оставь над исправлением комментарий:
       # БАГ: <что было не так>. ИСПРАВЛЕНИЕ: <что изменил и почему>.
    4. Поставь FIXED["имя_функции"] = True и запусти pytest tests/test_bugfix.py -k имя.
       Пока FIXED = False, тест считается «ещё не решённым».

В каждой функции ровно один баг, если в docstring не сказано другое.
"""

from collections.abc import Callable, Iterable
from typing import Any

FIXED = {
    "add_tag": False,
    "make_multipliers": False,
    "remove_negatives": False,
    "merge_config": False,
    "logged": False,
    "mean_and_max": False,
    "group_by_first_letter": False,
}


def add_tag(tag: str, tags: list[str] = []) -> list[str]:  # noqa: B006
    """Добавляет тег в список и возвращает его. Без второго аргумента — новый список.

    Жалоба: «Вызываю add_tag("a"), потом add_tag("b") и получаю ["a", "b"] вместо ["b"]».
    """
    tags.append(tag)
    return tags


def make_multipliers() -> list[Callable[[int], int]]:
    """Возвращает 4 функции: умножить на 0, на 1, на 2, на 3.

    Жалоба: «[m(2) for m in make_multipliers()] даёт [6, 6, 6, 6] вместо [0, 2, 4, 6]».
    """
    return [lambda x: x * i for i in range(4)]  # noqa: B023


def remove_negatives(nums: list[int]) -> list[int]:
    """Возвращает НОВЫЙ список без отрицательных чисел; входной список не меняется.

    Жалоба: «Для [-1, -2, 3] получаю [-2, 3], и мой исходный список тоже испортился».
    Здесь два бага.
    """
    for n in nums:
        if n < 0:
            nums.remove(n)
    return nums


def merge_config(base: dict, overrides: dict) -> dict:
    """Возвращает новый конфиг: base, поверх которого применены overrides
    (вложенные словари сливаются). base меняться не должен.

    Жалоба: «После merge_config мой DEFAULT_CONFIG изменился, и следующий запуск
    получил чужие настройки базы данных».
    """
    result = base.copy()
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key].update(value)
        else:
            result[key] = value
    return result


def logged(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор: дописывает имя вызванной функции в список CALL_LOG.

    Жалоба: «После декорирования все функции называются wrapper, и в логах
    pytest и в документации ничего не понять».
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        CALL_LOG.append(func.__name__)
        return func(*args, **kwargs)

    return wrapper


CALL_LOG: list[str] = []


def mean_and_max(values: Iterable[float]) -> tuple[float, float]:
    """Среднее и максимум. values может быть любым итерируемым, в том числе генератором.

    Жалоба: «С обычным списком работает, а с генератором падает с ZeroDivisionError».
    """
    total = sum(values)
    count = sum(1 for _ in values)
    return total / count, max(values)


def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:
    """Группирует слова по первой букве: {"a": ["apple", "avocado"], "b": ["banana"]}.

    Жалоба: «В каждой группе оказываются ВСЕ слова».
    """
    groups = dict.fromkeys({w[0] for w in words}, [])
    for w in words:
        groups[w[0]].append(w)
    return groups
