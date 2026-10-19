"""Паттерн 4. Стек.     [неделя 3]

СИГНАЛЫ: вложенность (скобки, выражения, k[...]), «отменить последнее»,
«ближайший больший / меньший элемент слева или справа», вычисление выражений.

ИДЕЯ: последний открытый закрывается первым (LIFO). Монотонный стек хранит
элементы, которые ещё «ждут» ответа, в упорядоченном виде; новый элемент снимает
со стека всех, для кого он и есть ответ. Каждый элемент кладётся и снимается
один раз -> O(n).
Аналогия: очередь на посадку по росту — пришёл высокий, и все ниже него
впереди «получили ответ» (их заслонили).
"""


def is_valid_brackets(s: str) -> bool:
    """LeetCode 20. Правильная ли скобочная последовательность из ()[]{}.

    >>> is_valid_brackets("([]{})")
    True
    >>> is_valid_brackets("(]")
    False
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack  # незакрытые скобки тоже ошибка


def eval_rpn(tokens: list[str]) -> int:
    """LeetCode 150. Вычислить выражение в обратной польской записи.
    Операции + - * /, деление целочисленное с округлением к нулю.

    >>> eval_rpn(["2", "1", "+", "3", "*"])
    9
    >>> eval_rpn(["4", "13", "5", "/", "+"])
    6
    """
    stack: list[int] = []
    for tok in tokens:
        if tok in {"+", "-", "*", "/"}:
            b, a = stack.pop(), stack.pop()  # порядок важен: a op b
            if tok == "+":
                stack.append(a + b)
            elif tok == "-":
                stack.append(a - b)
            elif tok == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))  # // округляет вниз: -7 // 2 == -4, а нужно -3
        else:
            stack.append(int(tok))
    return stack[0]


def daily_temperatures(temps: list[int]) -> list[int]:
    """LeetCode 739. Для каждого дня — через сколько дней станет теплее (0, если никогда).

    >>> daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])
    [1, 1, 4, 2, 1, 1, 0, 0]

    Цель: O(n). Монотонный стек индексов дней, ещё не нашедших более тёплый день.
    """
    answer = [0] * len(temps)
    stack: list[int] = []  # индексы; температуры в стеке убывают
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer


def decode_string(s: str) -> str:
    """LeetCode 394. Раскрыть запись вида k[строка], вложенность допустима.

    >>> decode_string("3[a]2[bc]")
    'aaabcbc'
    >>> decode_string("3[a2[c]]")
    'accaccacc'

    Подумай: что положить в стек при "[" и что достать при "]"?
    """
    stack: list[tuple[str, int]] = []
    current, number = "", 0
    for ch in s:
        if ch.isdigit():
            number = number * 10 + int(ch)  # числа бывают многозначными
        elif ch == "[":
            stack.append((current, number))  # запоминаем внешний контекст
            current, number = "", 0
        elif ch == "]":
            prev, k = stack.pop()
            current = prev + current * k
        else:
            current += ch
    return current


def largest_rectangle_area(heights: list[int]) -> int:
    """LeetCode 84 (hard). Площадь наибольшего прямоугольника в гистограмме.

    >>> largest_rectangle_area([2, 1, 5, 6, 2, 3])
    10

    Цель: O(n). Монотонный возрастающий стек: когда столбец снимается, справа от него
    первый более низкий (текущий), слева — тот, что под ним в стеке.
    """
    stack: list[int] = []
    best = 0
    for i, h in enumerate([*heights, 0]):  # 0 в конце снимает всё оставшееся
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best
