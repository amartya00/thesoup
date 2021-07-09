def merge(*arrays: list) -> list:
    """
    This function merges K individually sorted lists into a single sorted list. Complexity is `KNlog(N)`, where we are
    merging K arrays of N size each.
    :params arrays: A vararg of lists.
    :return: A new merged list.
    """
    if len(arrays) == 1:
        return arrays[0]
    semi_merged_list = list()
    for i in range(0, len(arrays)-1, 2):
        it1 = 0
        it2 = 0
        semi_merged_list.append(list())
        while it1 < len(arrays[i]) and it2 < len(arrays[i+1]):
            if arrays[i][it1] < arrays[i+1][it2]:
                semi_merged_list[-1].append(arrays[i][it1])
                it1 += 1
            else:
                semi_merged_list[-1].append(arrays[i+1][it2])
                it2 += 1
        while it1 < len(arrays[i]):
            semi_merged_list[-1].append(arrays[i][it1])
            it1 += 1
        while it2 < len(arrays[i+1]):
            semi_merged_list[-1].append(arrays[i+1][it2])
            it2 += 1
    if len(arrays) % 2 == 1:
        semi_merged_list.append(arrays[-1])
    return merge(*semi_merged_list)
