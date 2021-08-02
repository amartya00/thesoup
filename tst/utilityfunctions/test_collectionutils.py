import unittest

from thesoup.utilityfunctions.collectionutils import flatten, flatten_to_tuple, subsequence, foreach, transform
from thesoup.utilityclasses.sets import CountSet


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
            self.assertTrue(actual in expected_subs)

    def test_foreach(self):
        test_collection_1 = [1, 2, 3]
        call_tester_1 = []
        call = foreach(
            lambda item: item**2,
            test_collection_1
        ).then(
            lambda item: item + 1
        ).then(
            lambda item: item * (-1)
        ).then(
            lambda item: call_tester_1.append(item)
        )
        self.assertEqual(0, len(call_tester_1))
        call()
        self.assertEqual(
            [-2, -5, -10],
            call_tester_1
        )
        test_collection_2 = {1, 2, 3}
        call_tester_2 = set()
        call = foreach(
            lambda item: item ** 2,
            test_collection_2
        ).then(
            lambda item: item + 1
        ).then(
            lambda item: item * (-1)
        ).then(
            lambda item: call_tester_2.add(item)
        )
        self.assertEqual(0, len(call_tester_2))
        call()
        self.assertEqual(
            {-2, -5, -10},
            call_tester_2
        )

    def test_transform(self):
        my_list = [1, 2, 3, 4, 5]
        transformed_obj = transform(
            lambda item: item**2,
            my_list
        ).then(
            lambda item: item + 1
        ).then(
            lambda item: item * (-1)
        )
        transformed_list = list(transformed_obj)
        print(transformed_list)
        self.assertEqual(
            [-2, -5, -10, -17, -26],
            transformed_list
        )
