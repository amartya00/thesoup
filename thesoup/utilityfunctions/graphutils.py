from thesoup.utilityclasses.graph import DiGraph


def _topological_explore(graph: DiGraph, visited: set, stk: list, start):
    if start not in visited:
        visited.add(start)
        for c, _ in graph.get_neighbours(start):
            _topological_explore(graph, visited, stk, c)
        stk.append(start)


def topological_sort(graph: DiGraph) -> list:
    """
    This function returns a lost of vertices in a topologically sorted order.
    :param graph: A directed graph.
    :return: A list of sorted vertices.
    """
    vertices = graph.vertices()
    visited = set()
    stk = list()
    for v in vertices:
        _topological_explore(graph, visited, stk, v)
    return reversed(stk)
