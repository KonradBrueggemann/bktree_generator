# Konrad Brüggemann
# Universität Potsdam
# Bachelor Computerlinguistik
# 4. Semester


import unittest
from model.Distances import LevenshteinDistance, HammingDistance


class BKTreeTests:

    def __init__(self, tree):
        self.tree = tree

    def test_if_tree_is_correct(self):
        print("Testing tree for correctness...")
        return self._test_if_tree_is_correct(self.tree)

    def _test_if_tree_is_correct(self, tree):
        weights = []
        for child in tree.children:
            weights.append(child.weight)
            if weights.count(child.weight) > 1:
                return "Tree is not a BK tree!"

        else:
            for child in tree.children:
                self._test_if_tree_is_correct(child)
        return "No problems found."


class LevenshteinTests(unittest.TestCase):

    def test_insertion(self):
        result = LevenshteinDistance.dist("pran", "prank")
        self.assertEqual(result, 1)

    def test_lower_upper(self):
        result = LevenshteinDistance.dist("gap", "Gap")
        self.assertEqual(result, 1)

    def test_input_order(self):
        result_1 = LevenshteinDistance.dist("hello", "mellow")
        result_2 = LevenshteinDistance.dist("mellow", "hello")
        self.assertEqual(result_1, result_2)

    def test_complex_word(self):
        result = LevenshteinDistance.dist("copyright", "modesty")
        self.assertEqual(result, 8)


if __name__ == '__main__':
    unittest.main()
