from thesoup.utilityclasses.graph import Graph
from thesoup.utilityclasses.heap import MinHeap
from thesoup.utilityfunctions.collectionutils import flatten, flatten_to_tuple


def bfs(graph: Graph, start) -> dict:
    """
    This function implements bread first search on an object of type Graph. Complexity of such an algorithm is upper
    bound by `O(v)` where `v` is the number of vertices.

    It returns a map representing the predecessor relationship and "levels" of vertices. Example, consider the graph

    ```
    A -- B
     `-- C-- D
          `-- E
    ```

    Starting from A, the `bfs` function will return a map like this:
    {
      "A": (None, 0),
      "B": ("A", 1),
      "C": ("A", 1),
      "D": ("C", 2),
      "E": ("C",2)
    }
    This structure can be used to trace paths between the start to any reachable vertex.

    :param graph: The Digraph to traverse
    :param start: The starting point
    :return: A map of predecessors and levels.
    """
    predecessors = dict()
    if start in graph:
        predecessors[start] = (None, 0)
    else:
        return dict()
    frontier = {start}
    level = 1
    while len(frontier) > 0:
        next_frontier_unfiltered = flatten_to_tuple(
                [set(map(
                    lambda node: (node[0], (u, level)),
                    graph.get_neighbours(u)
                )) for u in frontier]
            )
        next_frontier = set(filter(
            lambda elem: elem[0] not in predecessors,
            next_frontier_unfiltered
        ))
        predecessors.update(next_frontier)
        frontier = set(
            map(
                lambda item: item[0],
                next_frontier
            )
        )
        level += 1
    return predecessors


def _dfs_callback(graph: Graph, start, parents: dict):
    for n in map(lambda x: x[0], graph.get_neighbours(start)):
        if n not in parents:
            parents[n] = start
            _dfs_callback(graph, n, parents)


def dfs(graph: Graph, start):
    """
    This implements depth first search on an object of type Graph. Complexity of such an algorithm is upper bound by
    `O(v)` where `v` is the number of vertices.

    It returns a map representing the predecessor relationship. Example consider the graph

    ```
    A -- B
     `-- C-- D
          `-- E
    ```

    Starting from A, the `dfs` function will return a map like this:
    {
      "A": None,
      "B": "A",
      "C": "A",
      "D": "C",
      "E": "C"
    }
    This structure can be used to trace paths between the start to any reachable vertex.


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

    NOTE: The input type is `Graph`. There is no separate interface for a di-graph in this library. Implementations of
    the `Graph` class must make it a di-graph. Otherwise this algorithm will hang.

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
