from thesoup.utilityclasses.graph import DiGraph, Edge
from thesoup.utilityfunctions.collectionutils import flatten


def bfs(graph: DiGraph, start):
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


def dfs_callback(graph: DiGraph, start, visited: set):
    if start not in graph:
        return set()
    nodes = {start}
    if start in visited:
        return set()
    else:
        visited.add(start)
        for n in map(lambda x: x[0], graph.get_neighbours(start)):
            nodes.update(dfs_callback(graph, n, visited))
    return nodes


def dfs(graph: DiGraph, start):
    visited = set()
    return dfs_callback(graph, start, visited)
