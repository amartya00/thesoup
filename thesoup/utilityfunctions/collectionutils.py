def flatten(item):
    """
    Recursively flattens a nested set of collections. Example
    (1, (2, 3)) would be flattened to [1,2,3]
    :param item: A possibly nested iterable
    :return: A flat list
    """
    if hasattr(item, "__iter__"):
        flattened = []
        for itm in item:
            flattened.extend(flatten(itm))
        return flattened
    else:
        return [item]
