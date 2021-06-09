from thesoup.utilityclasses.graph import Graph
from thesoup.utilityclasses.disjointsets import DisjointSets


def _topological_explore(graph: Graph, visited: set, stk: list, start):
    if start not in visited:
        visited.add(start)
        for c, _ in graph.get_neighbours(start):
            _topological_explore(graph, visited, stk, c)
        stk.append(start)


def topological_sort(graph: Graph) -> list:
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


def kruskal(graph: Graph) -> set:
    """
    This function implements the Kruskal's algorithm to find the min cost spanning tree of a di-graph
    :param graph: The input graph
    :return: A list of the edges comprising the MCST
    """
    sorted_edges = sorted(graph.edges())
    ds = DisjointSets(graph.vertices())
    selected_edges = set()

    for edge in sorted_edges:
        src, dest = edge.src, edge.destination
        if ds.find_set(src) != ds.find_set(dest):
            ds.union(src, dest)
        selected_edges.add(edge)
        if len(ds) == 1:
            break
    return selected_edges
