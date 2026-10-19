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
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def _find(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def words_with_prefix(self, prefix: str) -> list[str]:
        start = self._find(prefix)
        if start is None:
            return []
        result: list[str] = []
        stack = [(start, prefix)]
        while stack:  # DFS; детей кладём в обратном порядке, чтобы выдавать по алфавиту
            node, word = stack.pop()
            if node.is_word:
                result.append(word)
            for ch in sorted(node.children, reverse=True):
                stack.append((node.children[ch], word + ch))
        return result
