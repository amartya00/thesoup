import unittest

from thesoup.utilityclasses.disjointsets import DisjointSets


class TestDisjointSets (unittest.TestCase):
    def test_disjointsets(self):
        sample_data = ["a", "b", "c", "d", "e", "f"]
        test_ds = DisjointSets(sample_data)
        self.assertEqual(6, len(test_ds))
        for elem in sample_data:
            self.assertEqual(elem, test_ds.find_set(elem))

        test_ds.union('a', 'b')
        self.assertEqual('a', test_ds.find_set('b'))
        self.assertEqual('a', test_ds.find_set('a'))
        self.assertEqual(5, len(test_ds))

        test_ds.union('c', 'd')
        self.assertEqual('c', test_ds.find_set('c'))
        self.assertEqual('c', test_ds.find_set('d'))
        self.assertEqual(4, len(test_ds))

        test_ds.union('d', 'a')
        self.assertEqual('c', test_ds.find_set('a'))
        self.assertEqual('c', test_ds.find_set('b'))
        self.assertEqual('c', test_ds.find_set('c'))
        self.assertEqual('c', test_ds.find_set('d'))
        self.assertEqual(3, len(test_ds))