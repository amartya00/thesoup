import unittest

from thesoup.utilityclasses.binarytree import BinarySearchTree


class TestBinarySearchTree (unittest.TestCase):
    def test_insert_and_search(self):
        tree = BinarySearchTree()
        sample_data = [12, 1, 23, 36, 17, 6, 8, 44, 9]
        for item in sample_data:
            tree.insert(item)
        self.assertEqual(9, len(tree))
        for item in sample_data:
            self.assertTrue(item in tree)

    def test_deletes(self):
        tree = BinarySearchTree()
        sample_data = [12, 1, 23, 36, 17, 6, 8, 44, 9]
        for item in sample_data:
            tree.insert(item)
        del tree[12]
        self.assertEqual(8, len(tree))
        self.assertFalse(12 in tree)
        for elem in filter(lambda item : item != 12, sample_data):
            self.assertTrue(elem in tree)
        del tree[100]
        self.assertEqual(8, len(tree))

    def test_iterations(self):
        tree = BinarySearchTree()
        sample_data = [12, 1, 1, 23, 36, 36, 17, 6, 8, 44, 9]
        for item in sample_data:
            tree.insert(item)
        iterated_items = [item for item in tree]
        self.assertEqual(sorted(sample_data), iterated_items)
