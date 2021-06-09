from abc import ABC, abstractmethod


class Heap (ABC):
    def __init__(self):
        self.store = list()

    def __len__(self):
        return len(self.store)

    def __iter__(self):
        return iter(self.store)

    @abstractmethod
    def _compare(self, left, right) -> bool:
        pass

    @staticmethod
    def _get_parent(idx: int):
        return (idx - 1) // 2

    @staticmethod
    def _get_left_child(idx: int):
        return idx * 2 + 1

    @staticmethod
    def _get_right_child(idx: int):
        return idx * 2 + 2

    def _get_swappable_child(self, idx: int):
        left = Heap._get_left_child(idx)
        right = Heap._get_right_child(idx)
        if right >= len(self.store):
            return left
        else:
            return right if self._compare(
                self.store[left].__key__(), self.store[right].__key__()
            ) else left

    def _swap(self, left: int, right: int):
        tmp = self.store[left]
        self.store[left] = self.store[right]
        self.store[right] = tmp

    def _heapify(self, idx: int):
        # Bubble up if needed
        curr_idx = idx
        parent = Heap._get_parent(idx)
        while curr_idx > 0 and not self._compare(self.store[curr_idx].__key__(), self.store[parent].__key__()):
            self._swap(curr_idx, parent)
            curr_idx = parent
            parent = Heap._get_parent(curr_idx)

        # Bubble down if needed
        child = self._get_swappable_child(curr_idx)
        while child < len(self.store) and self._compare(self.store[curr_idx].__key__(), self.store[child].__key__()):
            self._swap(curr_idx, child)
            curr_idx = child
            child = self._get_swappable_child(curr_idx)

    def insert(self, elem):
        """
        Insert an element into the heap. The element has to have an attribute called `__key__`  which provides the key
        for comparison.
        :param elem: The element to insert into the heap
        :return
        """
        if not hasattr(elem, "__key__"):
            raise TypeError("{} does not define the __key__ attribute that is needed for heap operations")

        self.store.append(elem)
        self._heapify(len(self.store) - 1)

    def extract_extreme(self):
        """
        Extract the top of the heap
        """
        if len(self) == 0:
            return None
        elem = self.store[0]
        self.store[0] = self.store[-1]
        del self.store[-1]
        if len(self) > 0:
            self._heapify(0)
        return elem

    def get_extreme(self):
        """
        Returns the top element in the heap without extracting it
        """
        return self.store[0]

    def build_heap(self):
        """
        This re-builds the full heap. This is necessary if sometime there are many key updates for the heap elements
        externally and it is necessary to rebuild the whole heap.
        """
        for i in range(len(self) // 2, -1, -1):
            self._heapify(i)


class MinHeap (Heap):
    """
    Implements the min-heap data structure, where the element with the smallest key is always at the top if the heap.
    """
    def _compare(self, left, right) -> bool:
        return left >= right

    @staticmethod
    def from_iterable(collection):
        heap = MinHeap()
        for elem in collection:
            heap.insert(elem)
        return heap


class MaxHeap (Heap):
    """
    Implements the max-heap data structure, where the element with the largest key is always at the top if the heap.
    """
    def _compare(self, left, right) -> bool:
        return left <= right

    @staticmethod
    def from_iterable(collection):
        heap = MaxHeap()
        for elem in collection:
            heap.insert(elem)
        return heap