"""Префиксное дерево (Trie), LeetCode 208.

Задание: реализуй хранилище строк с быстрым поиском по префиксу.

Требования:
    - insert(word);
    - search(word) -> bool: слово было вставлено целиком;
    - starts_with(prefix) -> bool: есть хотя бы одно слово с этим префиксом;
    - words_with_prefix(prefix) -> list[str]: все такие слова в лексикографическом порядке
      (автодополнение в поисковой строке);
    - все операции за O(длина строки), не зависят от числа слов.

Подумай до кода:
    - Чем это лучше, чем set всех слов и перебор startswith?
    - Как отличить "app" как слово от "app" как префикса "apple"?
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
