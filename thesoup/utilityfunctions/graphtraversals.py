from thesoup.utilityclasses.graph import Graph
from thesoup.utilityclasses.heap import MinHeap
from thesoup.utilityfunctions.collectionutils import flatten


def bfs(graph: Graph, start):
    """
    This implements bread first search on an object of type DiGraph. Complexity of such an algorithm is upper bound by
    `O(v)` where `v` is the number of vertices.

    :param graph: The Digraph to traverse
    :param start: The starting point
    :return: A map of level vs traversed vertices.
    """
    levels = dict()
    visited = set()
    if start in graph:
        levels[0] = {start}
    else:
        return dict()
    frontier = set(map(lambda node: node[0], graph.get_neighbours(start)))
    level = 1
    while len(frontier) > 0:
        levels[level] = set()
        levels[level].update(frontier)
        visited.update(frontier)
        next_frontier = filter(
            lambda elem: elem not in visited,
            set(
                flatten(
                    [map(lambda node: node[0], graph.get_neighbours(n)) for n in frontier]
                )
            )
        )
        frontier = set(next_frontier)
        level += 1
    return levels


def _dfs_callback(graph: Graph, start, parents: dict):
    for n in map(lambda x: x[0], graph.get_neighbours(start)):
        if n not in parents:
            parents[n] = start
            _dfs_callback(graph, n, parents)


def dfs(graph: Graph, start):
    """
    This implements depth first search on an object of type DiGraph. Complexity of such an algorithm is upper bound by
    `O(v)` where `v` is the number of vertices.

    :param graph: The Digraph to traverse
    :param start: The starting point
    :return: A map of traversed vertices vs it's parents.
    """
    if start not in graph:
        return dict()
    parents = {start: None}
    _dfs_callback(graph, start, parents)
    return parents


def dijkstra(graph: Graph, start) -> (dict, dict):
    """
    This implements the dijkstra's algorithm fpr shortest path. It returns a tuple containing 2 dictionaries:
    a map of distances of vertices from `start` and another congaing the predecessor of each vertex.

    :param graph: The Digraph to traverse
    :param start: The starting point
    :return: A tuple (distances from start, predecessors).
    """
    if start not in graph:
        return dict(), dict()

    # Init
    d = dict([(v, float('inf')) for v in graph.vertices()])
    predecessors = dict([(v, None) for v in graph.vertices()])
    d[start] = 0

    class HeapElement:
        def __init__(self, vertex):
            self.vertex = vertex

        def __key__(self):
            return d[self.vertex]

    heap = MinHeap.from_iterable(list(map(lambda v: HeapElement(v), d.keys())))

    # Relax and repeat
    while len(heap) > 0:
        min_elem = heap.extract_extreme()
        u = min_elem.vertex
        for v, ppt in graph.get_neighbours(u):
            if d[v] > d[u] + ppt:
                d[v] = d[u] + ppt
                predecessors[v] = u
        heap.build_heap()
    return d, predecessors


def _shortest_path_dag_explorer(graph: Graph, predecessors: dict, memo: dict, start, end):
    if start == end:
        return 0
    elif (start, end) in memo:
        return memo[(start, end)]
    else:
        neighbours = graph.get_neighbours(start)
        if neighbours is None:
            return float('inf')
        if len(neighbours) == 0:
            return float('inf')
        sp, n = min(
            [(_shortest_path_dag_explorer(graph, predecessors, memo, n, end) + ppt, n) for n, ppt in neighbours]
        )
        if sp != float('inf'):
            memo[(start, end)] = sp
            predecessors[n] = start
        return sp


def shortest_path_dag(graph: Graph, start, end) -> (float, dict):
    """
    This function implements a special case SP algorithm for DAGs. Since it's a DAG, we can do this in a dynamic graph
    as well.
    NOTE: This
    :param graph: The Digraph to traverse
    :param start: The starting point
    :param end: The ending point
    :return: A tuple (shortest path, predecessors map).
    """
    memo = dict()
    predecessors = {start: None}
    sp = _shortest_path_dag_explorer(graph, predecessors, memo, start, end)
    return sp, predecessors
