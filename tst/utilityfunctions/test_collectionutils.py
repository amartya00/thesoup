import unittest

from thesoup.utilityfunctions.collectionutils import flatten, flatten_to_tuple, subsequence


class TestCollectionUtils (unittest.TestCase):
    def test_flatten(self):
        my_nested_collection = (1, (2, [1, 2, 3]), ("a", (1, 2)))
        self.assertEqual([1, 2, 1, 2, 3, "a", 1, 2], flatten(my_nested_collection))

    def test_flatten_tuple(self):
        my_nested_collection = [1, [2, (1, 2, 3)], ["a", (1, 2)]]
        self.assertEqual([1, 2, (1, 2, 3), "a", (1, 2)], flatten_to_tuple(my_nested_collection))

    def test_subsequence(self):
        sample_arr = [1, 2, 3]
        expected_subs = [
            [1],
            [2],
            [3],
            [1, 2],
            [2, 3],
            [1, 3],
            [1, 2, 3]
        ]
        actual_subsequences = subsequence(sample_arr)
        for actual in actual_subsequences:
            print(actual)
            self.assertTrue(actual in expected_subs)
