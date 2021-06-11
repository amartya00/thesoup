from abc import ABC, abstractmethod


class _BinaryTreeElement:
    """
    This class is meant to be used internally in a Binary Tree. Do not use it by itself
    """
    def __init__(self, val):
        self.val = val
        self.count = 1
        self.right = None
        self.left = None
        self.parent = None

    def __call__(self, *args, **kwargs):
        return self.val


class BinaryTree (ABC):
    """
    This is the interface for a binary tree
    """
    @abstractmethod
    def __contains__(self, item):
        """
        Method to check for an element in the tree

        :param item: The item to search
        :return: A boolean indicating presence
        """
        pass

    @abstractmethod
    def insert(self, item):
        """
        Method to insert an element in the tree

        :param item: The item to insert.
        :return:
        """
        pass

    @abstractmethod
    def __delitem__(self, key):
        """
        Method to delete an item from the tree

        :param item: The item to search and delete
        """
        pass

    @abstractmethod
    def __len__(self):
        """
        Method returning the size of the tree

        :return: The number of elements in the tree
        """
        pass

    @abstractmethod
    def __iter__(self):
        """
        Provide an iterator for a binary tree
        """
        pass


class BinarySearchTree (BinaryTree):
    """
    A BST implementation of a binary tree
    """
    def __init__(self):
        self.root = None
        self.num = 0

    @staticmethod
    def _insert(root: _BinaryTreeElement, element):
        if element > root():
            if root.right is not None:
                BinarySearchTree._insert(root.right, element)
            else:
                root.right = _BinaryTreeElement(element)
                root.right.parent = root
        elif element < root():
            if root.left is not None:
                BinarySearchTree._insert(root.left, element)
            else:
                root.left = _BinaryTreeElement(element)
                root.left.parent = root
        else:
            root.count += 1

    @staticmethod
    def _search(root: _BinaryTreeElement, item):
        iterator = root
        while iterator is not None:
            if iterator() == item:
                return iterator
            elif item > iterator():
                iterator = iterator.right
            else:
                iterator = iterator.left
        return None

    @staticmethod
    def _min(root: _BinaryTreeElement):
        iterator = root
        while iterator.left is not None:
            iterator = iterator.left
        return iterator

    @staticmethod
    def _max(root: _BinaryTreeElement):
        iterator = root
        while iterator.right is not None:
            iterator = iterator.right
        return iterator

    @staticmethod
    def _hard_delete(item: _BinaryTreeElement):
        if item.left is not None:
            max_left = BinarySearchTree._max(item.left)
            item.val = max_left.val
            item.count = max_left.count
            BinarySearchTree._hard_delete(max_left)
        elif item.right is not None:
            min_right = BinarySearchTree._min(item.right)
            item.val = min_right.val
            item.count = min_right.count
            BinarySearchTree._hard_delete(min_right)
        else:
            if item() < item.parent():
                item.parent.left = None
                del item
            else:
                item.parent.right = None
                del item

    @staticmethod
    def _next(root: _BinaryTreeElement):
        if root.right is not None:
            return BinarySearchTree._min(root.right)
        elif root.parent is not None:
            if root.parent() > root():
                return root.parent
            else:
                while root.parent is not None and root.parent() < root():
                    root = root.parent
                return root.parent
        else:
            return None

    def insert(self, item):
        if self.root is None:
            self.root = _BinaryTreeElement(item)
        else:
            BinarySearchTree._insert(self.root, item)
        self.num += 1

    def __len__(self):
        return self.num

    def __contains__(self, item):
        return BinarySearchTree._search(self.root, item) is not None

    def __delitem__(self, key):
        # Special case for root
        if key == self.root() and len(self) == 1:
            tmp = self.root
            self.root = None
            del tmp
            self.num = 0
        item = BinarySearchTree._search(self.root, key)
        if item is not None:
            BinarySearchTree._hard_delete(item)
            self.num -= 1

    def __iter__(self):
        class _BinarySearchTreeIterator:
            def __init__(self, root):
                self.pos = root
                self.pos_count = root.count

            def __next__(self):
                if self.pos is None:
                    raise StopIteration()
                elif self.pos_count > 1:
                    self.pos_count -= 1
                    return self.pos()
                else:
                    tmp = self.pos
                    self.pos = BinarySearchTree._next(self.pos)
                    if self.pos is not None:
                        self.pos_count = self.pos.count
                    return tmp()

        return _BinarySearchTreeIterator(
            BinarySearchTree._min(
                self.root
            )
        )