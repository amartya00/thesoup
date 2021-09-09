from inspect import getfullargspec


def flatten(item):
    """
    Recursively flattens a nested set of collections. Example
    (1, (2, 3)) would be flattened to [1,2,3]

    Dictionaries are flattened to tuples. Example
    {
            '213': {
                'abc': 'def',
                'xyz': 'ccc'
            },
            '214': {
                'abc': 'xyz',
                'papaya': [1, (2, 3)]
            }
        }
    would be flattened to
    [
        ('213', 'abc', 'def'),
        ('213', 'xyz', 'ccc'),
        ('214', 'abc', 'xyz'),
        ('214', 'papaya', 1),
        ('214', 'papaya', 2),
        ('214', 'papaya', 3)
    ]
    :param item: A possibly nested iterable
    :return: A flat list
    """
    if type(item) == str:
        return [item]
    elif type(item) == dict:
        flattened = []
        for k, v in item.items():
            flattened_values = flatten(v)
            for flattened_value in flattened_values:
                if type(flattened_value) != str and hasattr(flattened_value, '__iter__'):
                    flattened.append(
                        tuple(
                            [k] + [vv for vv in flattened_value]
                        )
                    )
                else:
                    flattened.append((k, flattened_value))
        return flattened
    elif hasattr(item, "__iter__"):
        flattened = []
        for itm in item:
            flattened.extend(flatten(itm))
        return flattened
    else:
        return [item]


def flatten_to_tuple(item):
    """
    Recursively flattens a nested set of collections, except tuples. Example
    (1, (2, 3)) would be flattened to [1,(2,3)]. However [[1, 2], [(3,4), 5] will
    be flattened to [1, 2, (3, 4), 5]

    Dictionaries are flattened to tuples. Example
    {
            '213': {
                'abc': 'def',
                'xyz': 'ccc'
            },
            '214': {
                'abc': 'xyz',
                'papaya': [1, (2, 3)]
            }
        }
    would be flattened to
    [
        ('213', ('abc', 'def')),
        ('213', ('xyz', 'ccc')),
        ('214', ('abc', 'xyz')),
        ('214', ('papaya', 1)),
        ('214', ('papaya', (2, 3)))
    ]

    :param item: A possibly nested iterable
    :return: A flat list
    """
    if type(item) == str:
        return [item]
    elif type(item) == tuple:
        return [item]
    elif type(item) == dict:
        flattened = []
        for k, v in item.items():
            flattened_values = flatten_to_tuple(v)
            for flattened_value in flattened_values:
                if type(flattened_value) != tuple and type(flattened_value) != str and hasattr(flattened_value, '__iter__'):
                    flattened.append(
                        tuple(
                            [k] + [vv for vv in flattened_value]
                        )
                    )
                else:
                    flattened.append((k, flattened_value))
        return flattened
    elif hasattr(item, "__iter__"):
        flattened = []
        for itm in item:
            flattened.extend(flatten_to_tuple(itm))
        return flattened
    else:
        return [item]


def _all_subsequences_from_idx(arr: list, start: int, memo: dict) -> list:
    if start in memo:
        return memo[start]
    start_elem = arr[start]
    all_subs = [[start_elem]]
    for it in range(start+1, len(arr)):
        sub_subsequences = _all_subsequences_from_idx(arr, it, memo)
        all_subs.extend(
            [[start_elem] + s for s in sub_subsequences]
        )
    memo[start] = all_subs
    return all_subs


def subsequence(arr: list) -> list:
    """
    This function returns all subsequences of a list. A subsequence is defined as any sublist of a list such that the
    elements in the subsequence are in the same order as the original list.
    Example: Subsequences of [1, 2, 3] are [1], [2], [3], [1, 2], [1, 3], [2, 3]

    :param arr: The list whose subsequences are needed.
    :return: A list of subsequences (list[list])
    """
    all_subs = []
    memo = dict()
    for it in range(len(arr)):
        all_subs.extend(_all_subsequences_from_idx(arr, it, memo))
    return all_subs


class _Foreach:
    def __init__(self, functor, iterable):
        num_args = len(getfullargspec(functor).args)
        if num_args != 1:
            raise TypeError(f"Passed function should take only 1 argument, instead it expects {num_args}.")
        if not hasattr(iterable, "__iter__"):
            raise TypeError(f"{iterable} is not iterable.")
        self._functors = [functor]
        self._iterable = iterable

    def then(self, functor):
        num_args = len(getfullargspec(functor).args)
        if num_args != 1:
            raise TypeError(f"Passed function should take only 1 argument, instead it expects {num_args}.")
        self._functors.append(functor)
        return self

    def __call__(self, *args, **kwargs):
        for item in self._iterable:
            temp = item
            for function in self._functors:
                temp = function(temp)


class _Transform:
    def __init__(self, functor, iterable):
        num_args = len(getfullargspec(functor).args)
        if num_args != 1:
            raise TypeError(f"Passed function should take only 1 argument, instead it expects {num_args}.")
        if not hasattr(iterable, "__iter__"):
            raise TypeError(f"{iterable} is not iterable.")
        self._functors = [functor]
        self._iterable = iterable
        self._internal_store = list()

    def then(self, functor):
        num_args = len(getfullargspec(functor).args)
        if num_args != 1:
            raise TypeError(f"Passed function should take only 1 argument, instead it expects {num_args}.")
        self._functors.append(functor)
        return self

    def __call__(self, *args, **kwargs):
        for item in self._iterable:
            transformed = None
            for function in self._functors:
                transformed = function(item)
            self._internal_store.append(transformed)

    def __iter__(self):
        class _TransformIterator:
            def __init__(self, collection, functors: list):
                self._functors = functors
                self._it = iter(collection)

            def __next__(self):
                raw_item = self._it.__next__()
                transformed_item = raw_item
                for f in self._functors:
                    transformed_item = f(transformed_item)
                return transformed_item
        return _TransformIterator(self._iterable, self._functors)


def foreach(functor, iterable):
    """
    This function allows the user to apply a method on each element of an iterable. Unlike `map`, there is no side
    effect. So you cannot use it to transform your iterable into a new one.

    This is lazily evaluated, and allows chaining using `then` function. You need to call the `()` method to start
    evaluation.

    Example
    -------
    ```
    my_list = [1, 2, 3]
    foreach(lambda item: print(f"Parsing {item} in f1"), my_list)
        .then(lambda item: print(f"Parsing {item} in f2"))
        .then(lambda item: print(f"Parsing {item} in f3"))()

    Output will be
    Parsing 1 in f1
    Parsing 1 in f2
    Parsing 1 in f3
    Parsing 2 in f1 .....

    :param functor: The function to apply gto each element in an iterable.
    :param iterable: The iterable under processing.
    :return: A _ForEach object (this is internal). Just use the `.then` method to chain or just call it `()` to start
    execution.
    ```
    """
    return _Foreach(functor, iterable)


# TODO: Add filter capabilities
def transform(functor, iterable):
    """
    This function allows the user to apply a method on each element of an iterable, and produce a new one. The
    difference between this and Python's build in `map` function is that this allows chaining using `then` function.

    Example
    -------
    ```
    my_list = [1, 2, 3]
    transformed = transform(
            lambda item: item**2,
            my_list
        ).then(
            lambda item: item + 1
        ).then(
            lambda item: item * (-1)
        )
    transformed_list = list(transformed)
    print(transformed_list)

    Output will be
    [-2, -5, -10]

    :param functor: The function to apply gto each element in an iterable.
    :param iterable: The iterable under processing.
    :return: A _Transform object (this is internal). Just use the `.then` method to chain more transformer functions.
    You can pass the returned object to the constructor of any iterable just like you would with a `map` object.

    ```
    """
    return _Transform(functor, iterable)
