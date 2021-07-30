class CountSet:
    """
    This class implements a set where if multiple elements are inserted, the set keeps track of counts.
    It supports the usual set functionality like add, update, etc. Along with that it also supports access with square
    brackets (__getitem__) that returns the count of an element. If absent, 0 is returned
    """
    def __init__(self, iterable=None):
        self.num = 0
        self.store = dict()
        if iterable is not None:
            for elem in iterable:
                self.add(elem)

    def _add_many(self, items: list):
        for item, count in items:
            if item in self.store:
                self.store[item] += count
            else:
                self.store[item] = count
            self.num += count

    def add(self, item):
        """
        Method to add an item to the set.

        :param item: The item to add
        :return: Void
        """
        if item not in self.store:
            self.store[item] = 1
        else:
            self.store[item] += 1
        self.num += 1

    def update(self, items):
        """
        Method to add many items to the set.

        :param items: The iterable of items to add
        :return: Void
        """
        for item in items:
            self.add(item)

    def __contains__(self, item) -> bool:
        return item in self.store

    def __getitem__(self, item) -> int:
        return 0 if item not in self.store else self.store[item]

    def __add__(self, other: 'CountSet') -> 'CountSet':
        if type(other) != CountSet:
            raise TypeError(f"Cannot add {type(other)} with CountSet object")
        added = CountSet()
        added.store = self.store.copy()
        added.num = self.num
        added._add_many(other.store.items())
        return added

    def __iter__(self):
        return iter(self.store.items())

    def __delitem__(self, key):
        if key in self.store:
            if self.store[key] == 1:
                del self.store[key]
            else:
                self.store[key] -= 1
            self.num -= 1

    def __eq__(self, other):
        return type(other) == CountSet and self.store == other.store

    def __len__(self):
        return self.num
