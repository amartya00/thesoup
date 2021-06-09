import unittest
import random

from thesoup.utilityclasses.heap import MaxHeap, MinHeap


class IntegerHeapElem:
    def __init__(self, val: int):
        self.val = val

    def __key__(self):
        return self.val


class TestMinHeap (unittest.TestCase):
    def test_inserts(self):
        sample_elements = [1, 4, 2, 10, 7, 6, 19, 2, 4]
        test_heap = MinHeap.from_iterable(list(map(lambda x: IntegerHeapElem(x), sample_elements)))
        self.assertEqual(1, test_heap.get_extreme().__key__())

    def test_extract_min(self):
        sample_elements = [1, 4, 2, 10, 7, 6, 19, 2, 4]
        test_heap = MinHeap.from_iterable(list(map(lambda x: IntegerHeapElem(x), sample_elements)))
        results = []
        while len(test_heap) > 0:
            results.append(test_heap.extract_extreme().__key__())
        self.assertEqual(sorted(sample_elements), results)

    def test_build_heap(self):
        test_heap = MinHeap()
        sample_data = [1, 4, 2, 10, 7, 6, 19, 2, 4]
        test_heap.store = [IntegerHeapElem(e) for e in sample_data]
        test_heap.build_heap()
        results = []
        while len(test_heap) > 0:
            results.append(test_heap.extract_extreme().__key__())
        self.assertEqual(sorted(sample_data), results)

    def test_smoke(self):
        test_heap = MinHeap()
        sample_elements = [random.randint(1, 1000) for _ in range(50)]
        [test_heap.insert(IntegerHeapElem(e)) for e in sample_elements]
        results = []
        while len(test_heap) > 0:
            results.append(test_heap.extract_extreme().__key__())
        self.assertEqual(sorted(sample_elements), results)


class TestMaxHeap (unittest.TestCase):
    def test_inserts(self):
        sample_elements = [1, 4, 2, 10, 7, 6, 19, 2, 4]
        test_heap = MaxHeap.from_iterable(list(map(lambda x: IntegerHeapElem(x), sample_elements)))
        self.assertEqual(19, test_heap.get_extreme().__key__())

    def test_extract_min(self):
        sample_elements = [1, 4, 2, 10, 7, 6, 19, 2, 4]
        test_heap = MaxHeap.from_iterable(list(map(lambda x: IntegerHeapElem(x), sample_elements)))
        results = []
        while len(test_heap) > 0:
            results.append(test_heap.extract_extreme().__key__())
        self.assertEqual(sorted(sample_elements, reverse=True), results)

    def test_build_heap(self):
        test_heap = MaxHeap()
        sample_data = [1, 4, 2, 10, 7, 6, 19, 2, 4]
        test_heap.store = [IntegerHeapElem(e) for e in sample_data]
        test_heap.build_heap()
        results = []
        while len(test_heap) > 0:
            results.append(test_heap.extract_extreme().__key__())
        self.assertEqual(sorted(sample_data, reverse=True), results)

    def test_smoke(self):
        test_heap = MaxHeap()
        sample_elements = [random.randint(1, 1000) for _ in range(50)]
        [test_heap.insert(IntegerHeapElem(e)) for e in sample_elements]
        results = []
        while len(test_heap) > 0:
            results.append(test_heap.extract_extreme().__key__())
        self.assertEqual(sorted(sample_elements, reverse=True), results)
