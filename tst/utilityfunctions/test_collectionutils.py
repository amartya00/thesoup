import unittest

from thesoup.utilityfunctions.collectionutils import flatten


class TestCollectionUtils (unittest.TestCase):
    def test_flatten(self):
        my_nested_collection = (1, (2, [1, 2, 3]), ("a", (1, 2)))
        self.assertEqual([1, 2, 1, 2, 3, "a", 1, 2], flatten(my_nested_collection))
