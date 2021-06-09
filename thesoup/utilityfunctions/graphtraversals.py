from thesoup.utilityclasses.graph import DiGraph
from thesoup.utilityclasses.heap import MinHeap
from thesoup.utilityfunctions.collectionutils import flatten


def bfs(graph: DiGraph, start):
    """
    This implements bread first search on an object of type DiGraph. Complexity of such an algorithm is upper bound by
    `O(v)` where `v` is the number of vertices.
    """
    v_set = set()
    visited = set()
    if start in graph:
        v_set.add(start)
    else:
        return set()
    frontier = set(map(lambda node: node[0], graph.get_neighbours(start)))

    while len(frontier) > 0:
        v_set.update(frontier)
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
    return v_set


def _dfs_callback(graph: DiGraph, start, visited: set):
    if start not in graph:
        return set()
    nodes = {start}
    if start in visited:
        return set()
    else:
        visited.add(start)
        for n in map(lambda x: x[0], graph.get_neighbours(start)):
            nodes.update(_dfs_callback(graph, n, visited))
    return nodes


def dfs(graph: DiGraph, start):
    """
    This implements depth first search on an object of type DiGraph. Complexity of such an algorithm is upper bound by
    `O(v)` where `v` is the number of vertices.
    """
    visited = set()
    return _dfs_callback(graph, start, visited)


def dijkstra(graph: DiGraph, start) -> tuple:
    """
    This implements the dijkstra's algorithm fpr shortest path
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
