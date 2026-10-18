"""Тесты паттернов 6–11: списки, деревья, куча, графы, перебор, динамика."""

import random
import statistics
from itertools import combinations, pairwise, permutations

from algorithms import p06_linked_list as ll
from algorithms import p07_trees as tr
from algorithms import p08_heap as hp
from algorithms import p09_graphs as gr
from algorithms import p10_backtracking as bt
from algorithms import p11_dp as dp

rng = random.Random(7)

# ---------------------------------------------------------------- p06 linked list


def test_reverse_list():
    assert ll.to_list(ll.reverse_list(ll.from_list([1, 2, 3, 4]))) == [4, 3, 2, 1]
    assert ll.reverse_list(None) is None


def test_merge_two_lists():
    merged = ll.merge_two_lists(ll.from_list([1, 2, 4]), ll.from_list([1, 3, 4]))
    assert ll.to_list(merged) == [1, 1, 2, 3, 4, 4]
    assert ll.to_list(ll.merge_two_lists(None, ll.from_list([0]))) == [0]


def test_has_cycle():
    head = ll.from_list([3, 2, 0, -4])
    assert not ll.has_cycle(head)
    tail = head
    while tail.next:
        tail = tail.next
    tail.next = head.next  # хвост указывает на второй узел
    assert ll.has_cycle(head)
    assert not ll.has_cycle(None)


def test_middle_node():
    assert ll.to_list(ll.middle_node(ll.from_list([1, 2, 3, 4, 5]))) == [3, 4, 5]
    assert ll.to_list(ll.middle_node(ll.from_list([1, 2, 3, 4, 5, 6]))) == [4, 5, 6]


def test_remove_nth_from_end():
    assert ll.to_list(ll.remove_nth_from_end(ll.from_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    assert ll.to_list(ll.remove_nth_from_end(ll.from_list([1]), 1)) == []
    assert ll.to_list(ll.remove_nth_from_end(ll.from_list([1, 2]), 2)) == [2]  # удаляется голова


# ---------------------------------------------------------------- p07 trees

TREE = [3, 9, 20, None, None, 15, 7]


def test_max_depth_and_level_order():
    assert tr.max_depth(tr.from_level_order(TREE)) == 3
    assert tr.max_depth(None) == 0
    assert tr.level_order(tr.from_level_order(TREE)) == [[3], [9, 20], [15, 7]]
    assert tr.level_order(None) == []


def test_invert_and_same_tree():
    inverted = tr.invert_tree(tr.from_level_order([4, 2, 7, 1, 3, 6, 9]))
    assert tr.is_same_tree(inverted, tr.from_level_order([4, 7, 2, 9, 6, 3, 1]))
    assert not tr.is_same_tree(tr.from_level_order([1, 2]), tr.from_level_order([1, None, 2]))
    assert tr.is_same_tree(None, None)


def test_is_valid_bst():
    assert tr.is_valid_bst(tr.from_level_order([2, 1, 3]))
    assert not tr.is_valid_bst(tr.from_level_order([5, 1, 4, None, None, 3, 6]))
    assert not tr.is_valid_bst(tr.from_level_order([5, 1, 6, None, None, 3, 7]))  # ловушка
    assert not tr.is_valid_bst(tr.from_level_order([2, 2, 2]))  # дубликаты недопустимы


def test_lowest_common_ancestor_bst():
    root = tr.from_level_order([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    assert tr.lowest_common_ancestor_bst(root, 2, 8) == 6
    assert tr.lowest_common_ancestor_bst(root, 2, 4) == 2
    assert tr.lowest_common_ancestor_bst(root, 3, 5) == 4


def test_diameter():
    assert tr.diameter(tr.from_level_order([1, 2, 3, 4, 5])) == 3
    assert tr.diameter(tr.from_level_order([1, 2])) == 1
    # Самый длинный путь не через корень
    deep = [1, 2, None, 3, 4, 5, None, None, 6, 7, None, None, 8]
    assert tr.diameter(tr.from_level_order(deep)) == 6


# ---------------------------------------------------------------- p08 heap


def test_kth_largest():
    assert hp.kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert hp.kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    for _ in range(50):
        nums = [rng.randint(-50, 50) for _ in range(rng.randint(1, 30))]
        k = rng.randint(1, len(nums))
        assert hp.kth_largest(nums, k) == sorted(nums, reverse=True)[k - 1]


def test_k_closest():
    assert hp.k_closest([(1, 3), (-2, 2)], 1) == [(-2, 2)]
    assert hp.k_closest([(3, 3), (5, -1), (-2, 4)], 2) == [(3, 3), (-2, 4)]


def test_merge_k_sorted():
    assert hp.merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert hp.merge_k_sorted([]) == [] and hp.merge_k_sorted([[], [1]]) == [1]


def test_last_stone_weight():
    assert hp.last_stone_weight([2, 7, 4, 1, 8, 1]) == 1
    assert hp.last_stone_weight([2, 2]) == 0


def test_median_finder():
    mf = hp.MedianFinder()
    seen = []
    for _ in range(200):
        x = rng.randint(-100, 100)
        mf.add_num(x)
        seen.append(x)
        assert mf.find_median() == statistics.median(seen)


# ---------------------------------------------------------------- p09 graphs


def test_num_islands():
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    snapshot = [row.copy() for row in grid]
    assert gr.num_islands(grid) == 3
    assert grid == snapshot  # входные данные не изменены
    assert gr.num_islands([["1"] * 300 for _ in range(300)]) == 1  # без переполнения рекурсии


def test_shortest_path_grid():
    assert gr.shortest_path_grid([[0, 1], [1, 0]]) == 2
    assert gr.shortest_path_grid([[0, 0, 0], [1, 1, 0], [1, 1, 0]]) == 4
    assert gr.shortest_path_grid([[1, 0, 0], [1, 1, 0], [1, 1, 0]]) == -1


def test_course_order():
    assert gr.course_order(2, [(1, 0)]) == [0, 1]
    assert gr.course_order(4, [(1, 0), (2, 0), (3, 1), (3, 2)]) == [0, 1, 2, 3]
    assert gr.course_order(2, [(1, 0), (0, 1)]) == []
    assert gr.can_finish(3, [(1, 0), (2, 1)])
    assert not gr.can_finish(3, [(1, 0), (2, 1), (0, 2)])


def test_count_components():
    assert gr.count_components(5, [(0, 1), (1, 2), (3, 4)]) == 2
    assert gr.count_components(5, [(0, 1), (1, 2), (2, 3), (3, 4)]) == 1
    assert gr.count_components(3, []) == 3


def test_network_delay():
    assert gr.network_delay([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2) == 2
    assert gr.network_delay([(1, 2, 1)], 2, 2) == -1
    assert gr.network_delay([(1, 2, 5), (1, 3, 1), (3, 2, 1)], 3, 1) == 2  # обходной путь короче


# ---------------------------------------------------------------- p10 backtracking


def test_subsets_and_permutations():
    assert bt.subsets([1, 2]) == [[], [1], [1, 2], [2]]
    nums = [1, 2, 3, 4]
    expected = sorted(list(c) for r in range(5) for c in combinations(nums, r))
    assert bt.subsets(nums) == expected
    assert bt.permutations([1, 2, 3]) == sorted(list(p) for p in permutations([1, 2, 3]))
    assert len(bt.permutations([1, 2, 3, 4, 5])) == 120


def test_combination_sum():
    assert bt.combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
    assert bt.combination_sum([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert bt.combination_sum([2], 1) == []


def test_generate_parentheses():
    assert bt.generate_parentheses(1) == ["()"]
    assert bt.generate_parentheses(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert len(bt.generate_parentheses(5)) == 42  # числа Каталана


def test_word_search():
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    snapshot = [row.copy() for row in board]
    assert bt.word_search(board, "ABCCED")
    assert bt.word_search(board, "SEE")
    assert not bt.word_search(board, "ABCB")  # клетку нельзя использовать дважды
    assert board == snapshot


# ---------------------------------------------------------------- p11 dp


def test_climb_stairs():
    assert [dp.climb_stairs(n) for n in range(1, 8)] == [1, 2, 3, 5, 8, 13, 21]
    assert dp.climb_stairs(45) == 1836311903


def test_rob():
    assert dp.rob([1, 2, 3, 1]) == 4
    assert dp.rob([2, 7, 9, 3, 1]) == 12
    assert dp.rob([]) == 0


def test_coin_change():
    assert dp.coin_change([1, 2, 5], 11) == 3
    assert dp.coin_change([2], 3) == -1
    assert dp.coin_change([1], 0) == 0
    assert dp.coin_change([1, 3, 4], 6) == 2  # жадный алгоритм дал бы 3 (4+1+1)


def test_length_of_lis():
    assert dp.length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert dp.length_of_lis([7, 7, 7]) == 1
    for _ in range(100):
        nums = [rng.randint(0, 10) for _ in range(rng.randint(0, 10))]
        brute = max(
            [
                r
                for r in range(len(nums) + 1)
                for c in combinations(nums, r)
                if all(a < b for a, b in pairwise(c))
            ]
            + [0]
        )
        assert dp.length_of_lis(nums) == brute


def test_lcs_and_edit_distance():
    assert dp.longest_common_subsequence("abcde", "ace") == 3
    assert dp.longest_common_subsequence("abc", "def") == 0
    assert dp.edit_distance("horse", "ros") == 3
    assert dp.edit_distance("intention", "execution") == 5
    assert dp.edit_distance("", "abc") == 3


def test_unique_paths():
    assert dp.unique_paths(3, 7) == 28
    assert dp.unique_paths(3, 2) == 3
    assert dp.unique_paths(1, 1) == 1
