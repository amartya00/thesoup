import unittest

from thesoup.utilityclasses.sets import CountSet


class TestSets (unittest.TestCase):
    def setUp(self) -> None:
        self.arr1 = [1, 1, 2, 2, 2, 3, 3, 4, 5]
        self.arr2 = [1, 1, 2, 2, 2, 3, 3, 4, 5, 5]
        self.c1 = CountSet(self.arr1)
        self.c2 = CountSet(self.arr1)
        self.c3 = CountSet(self.arr2)

    def test_count_sets_constructor(self):
        self.assertEqual(self.c1, self.c2)
        self.assertNotEqual(self.c1, self.c3)
        self.assertNotEqual(self.c2, self.c3)

    def test_count_sets_lengths(self):
        self.assertEqual(len(self.arr1), len(self.c1))
        self.assertEqual(len(self.arr1), len(self.c2))
        self.assertEqual(len(self.arr2), len(self.c3))

    def test_count_sets_adds(self):
        s1 = {1, 2, 3}
        self.assertEqual(2, self.c1[1])
        self.assertEqual(3, self.c1[2])
        self.assertEqual(2, self.c1[3])

        self.c1.update(s1)

        self.assertEqual(3, self.c1[1])
        self.assertEqual(4, self.c1[2])
        self.assertEqual(3, self.c1[3])
        self.assertEqual(len(self.arr1) + len(s1), len(self.c1))

        self.c1.add(3)
        self.assertEqual(4, self.c1[3])
        c3 = CountSet(self.arr1 + self.arr2)
        self.assertEqual(c3, self.c2 + self.c3)
        self.assertEqual(len(self.arr1) + len(s1) + 1, len(self.c1))

    def test_count_sets_delete(self):
        self.assertEqual(len(self.arr1), len(self.c1))
        self.assertEqual(2, self.c1[1])
        del self.c1[1]
        self.assertEqual(len(self.arr1) - 1, len(self.c1))
        self.assertEqual(1, self.c1[1])
        del self.c1[1]
        self.assertEqual(len(self.arr1) - 2, len(self.c1))
        self.assertEqual(0, self.c1[1])
        del self.c1[1]
        self.assertEqual(len(self.arr1) - 2, len(self.c1))
        self.assertEqual(0, self.c1[1])
        del self.c1[1]
        self.assertEqual(len(self.arr1) - 2, len(self.c1))
        self.assertEqual(0, self.c1[1])
        del self.c1[2]
        self.assertEqual(len(self.arr1) - 3, len(self.c1))
        self.assertEqual(2, self.c1[2])

    def test_count_sets_iter(self):
        expected_pairs = {(1, 2), (2, 3), (3, 2), (4, 1), (5, 1)}
        for w, c in self.c1:
            self.assertTrue((w, c) in expected_pairs)
