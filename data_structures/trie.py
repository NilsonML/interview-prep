"""Префиксное дерево (Trie), LeetCode 208.     [обязательно · неделя 7]

ИНТУИЦИЯ
    Автодополнение в поиске: печатаешь «app» — и сразу видишь apple, apply.
    Слова с общим началом делят общий путь в дереве, каждая буква — шаг вниз.

КАК УСТРОЕНО (слова: app, apple, apply, bat)
    root
     ├─ a ─ p ─ p* ─ l ─ e*
     │                └─ y*
     └─ b ─ a ─ t*                 * = здесь заканчивается слово (is_word)

    search("app")       идём a -> p -> p, узел помечен * -> True
    search("appl")      путь есть, но * нет -> False (это только префикс)
    starts_with("ap")   путь есть -> True
    Время зависит от длины слова, а не от числа слов в словаре.

ТЕРМИНЫ: префикс, узел, флаг конца слова, DFS для перечисления слов.

ЗАДАНИЕ
    - insert(word); search(word) -> bool; starts_with(prefix) -> bool;
    - words_with_prefix(prefix) -> list[str] в лексикографическом порядке;
    - все операции за O(длина строки).
"""


class TrieNode:
    """Узел дерева: словарь детей и флаг конца слова. Уже реализован, можно менять."""

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False  # здесь заканчивается вставленное слово


class Trie:
    def __init__(self) -> None:
        raise NotImplementedError

    def insert(self, word: str) -> None:
        raise NotImplementedError

    def search(self, word: str) -> bool:
        raise NotImplementedError

    def starts_with(self, prefix: str) -> bool:
        raise NotImplementedError

    def words_with_prefix(self, prefix: str) -> list[str]:
        raise NotImplementedError
