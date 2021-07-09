import unittest

from thesoup.utilityfunctions.merge import merge
from thesoup.utilityfunctions.collectionutils import flatten


class TestMerge (unittest.TestCase):
    def test_k_way_merge(self):
        l1 = [1, 3, 45, 188, 200]
        l2 = [2, 4, 5, 7, 99, 102, 144, 199]
        l3 = [12, 13, 14, 15]
        l4 = [100, 200, 300, 400, 500, 600, 800, 900]
        l5 = [1, 2, 3]
        l6 = [1, 2, 3]
        l7 = [1, 100, 101, 102, 999, 1000, 1001, 3000]
        expected_list = sorted(flatten([l1, l2, l3, l4, l5, l6, l7]))
        actual_list = merge(l1, l2, l3, l4, l5, l6, l7)
        self.assertEqual(expected_list, actual_list)

    def test_k_way_merge_order_independent(self):
        l1 = [1, 3, 45, 188, 200]
        l2 = [2, 4, 5, 7, 99, 102, 144, 199]
        l3 = [12, 13, 14, 15]
        l4 = [100, 200, 300, 400, 500, 600, 800, 900]
        l5 = [1, 2, 3]
        l6 = [1, 2, 3]
        l7 = [1, 100, 101, 102, 999, 1000, 1001, 3000]
        expected_list = sorted(flatten([l1, l2, l3, l4, l5, l6, l7]))
        actual_1 = merge(l1, l2, l3, l4, l5, l6, l7)
        actual_2 = merge(l1, l3, l2, l7, l5, l6, l4)
        actual_3 = merge(l2, l3, l1, l5, l7, l6, l4)
        self.assertEqual(expected_list, actual_1)
        self.assertEqual(actual_1, actual_2)
        self.assertEqual(actual_2, actual_3)

