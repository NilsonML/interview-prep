"""Паттерн 2. Два указателя.     [неделя 2]

СИГНАЛЫ: массив отсортирован (или его можно отсортировать); найти пару / тройку
с условием на сумму; палиндром; «на месте, O(1) памяти»; слить два списка.

ИДЕЯ: два индекса двигаются навстречу (или один быстрее другого). Каждый шаг
доказуемо отбрасывает варианты, которые не могут быть ответом, поэтому O(n) вместо O(n^2).
Аналогия: ищешь в отсортированной стопке две купюры на нужную сумму — если мало,
берёшь купюру побольше слева, если много — поменьше справа.

РАЗНОВИДНОСТИ: навстречу друг другу (сумма, палиндром, контейнер с водой);
«медленный и быстрый» в одну сторону (удалить дубликаты на месте); по двум массивам (слияние).
"""


def is_palindrome(s: str) -> bool:
    """LeetCode 125. Палиндром ли строка, если учитывать только буквы и цифры без регистра.

    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    >>> is_palindrome("race a car")
    False

    Цель: O(n) времени, O(1) памяти (без создания очищенной копии).
    """
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        elif s[left].lower() != s[right].lower():
            return False
        else:
            left += 1
            right -= 1
    return True


def two_sum_sorted(numbers: list[int], target: int) -> tuple[int, int]:
    """LeetCode 167. Массив отсортирован по возрастанию. Индексы i < j с суммой target
    (нумерация с 0). Решение существует.

    >>> two_sum_sorted([2, 7, 11, 15], 9)
    (0, 1)

    Цель: O(n) времени и O(1) памяти — без словаря.
    Подумай: сумма меньше target — какой указатель сдвинуть и почему это безопасно?
    """
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return left, right
        if s < target:
            left += 1  # numbers[left] с любым другим правым даст ещё меньше — отбрасываем
        else:
            right -= 1
    raise ValueError("no solution")


def three_sum(nums: list[int]) -> list[list[int]]:
    """LeetCode 15. Все УНИКАЛЬНЫЕ тройки с суммой 0. Каждая тройка отсортирована,
    список троек отсортирован.

    >>> three_sum([-1, 0, 1, 2, -1, -4])
    [[-1, -1, 2], [-1, 0, 1]]

    Цель: O(n^2). Подумай: зафиксируй первый элемент — что осталось решить?
    Как пропускать дубликаты без set?
    """
    nums = sorted(nums)
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # такой первый элемент уже рассматривали
        if nums[i] > 0:
            break  # дальше все положительные, сумма не может быть 0
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s < 0:
                left += 1
            elif s > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                right -= 1
    return result


def max_area(height: list[int]) -> int:
    """LeetCode 11. Контейнер с наибольшим объёмом воды между двумя линиями.

    >>> max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])
    49

    Цель: O(n). Подумай: почему всегда двигаем указатель с МЕНЬШЕЙ высотой?
    """
    left, right, best = 0, len(height) - 1, 0
    while left < right:
        best = max(best, (right - left) * min(height[left], height[right]))
        # Объём ограничен меньшей стенкой. Сдвинув большую, ширина уменьшится,
        # а высота не вырастет выше меньшей стенки -> лучше не станет.
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best


def remove_duplicates(nums: list[int]) -> int:
    """LeetCode 26. Удалить дубликаты из отсортированного массива НА МЕСТЕ.
    Вернуть k — число уникальных; первые k элементов nums должны быть уникальными
    по возрастанию.

    >>> a = [0, 0, 1, 1, 1, 2]
    >>> remove_duplicates(a), a[:3]
    (3, [0, 1, 2])

    Цель: O(n), O(1) памяти. Паттерн «медленный и быстрый указатель».
    """
    if not nums:
        return 0
    write = 1  # куда писать следующий уникальный
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write


def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    """Слить два отсортированных списка в один отсортированный (основа merge sort, LeetCode 88).

    >>> merge_sorted([1, 3, 5], [2, 4])
    [1, 2, 3, 4, 5]

    Цель: O(len(a) + len(b)), без sorted().
    """
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:  # <= сохраняет порядок равных (устойчивость)
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result
