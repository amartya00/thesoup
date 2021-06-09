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
