from inspect import getfullargspec

def flatten(item):
    """
    Recursively flattens a nested set of collections. Example
    (1, (2, 3)) would be flattened to [1,2,3]
    :param item: A possibly nested iterable
    :return: A flat list
    """
    if type(item) == str:
        return [item]
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
    :param item: A possibly nested iterable
    :return: A flat list
    """
    if type(item) == str:
        return [item]
    elif type(item) == tuple:
        return [item]
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
            for function in self._functors:
                function(item)


def foreach(functor, iterable):
    """
    This function allows the user to apply a method on each element of an iterable. Unlike `map`, there is no side effect.
    So you cannot use it to transform your iterable into a new one.

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