import json
from abc import ABC, abstractmethod
from thesoup.utilityfunctions.collectionutils import flatten


class Edge:
    """
    This class is meant to represent an edge of a graph. It has 3 members: source, destination and a "property". This
    is left vague on purpose. Use the "property" to indicate weight or something else if you like.

    All the 3 members must define the `__str__` and `__eq__` methods.
    """
    def __init__(self, src, destination, ppt):
        self.src = src
        self.destination = destination
        self.ppt = ppt

    def __hash__(self) -> int:
        return int(
            hash(
                "{}.{}.{}".format(self.src, self.destination, self.ppt)
            )
        )

    def __eq__(self, other) -> bool:
        return type(other) == Edge and \
               self.src == other.src and \
               self.destination == other.destination and \
               other.ppt == self.ppt

    def __str__(self):
        return "{}.{}.{}".format(self.src, self.destination, self.ppt)

    def __gt__(self, other):
        if type(other) != Edge:
            raise TypeError("Cannot compare edge to non edge")
        return self.ppt > other.ppt


class Graph (ABC):
    """
    This is the interface for a directed graph
    """
    @abstractmethod
    def get_neighbours(self, item) -> list:
        """
        Returns the neighbours of a vertex
        :param item: Vertex whose neighbours to fetch
        :return:
        """
        pass

    @abstractmethod
    def __contains__(self, item):
        """
        Returns if a vertex or an edge exists in the graph.
        NOTE: To test the existence of an edge, pass an object of `Edge` type
        :param item: the vertex or edge to test
        :return:
        """
        pass

    @abstractmethod
    def vertices(self) -> set:
        """
        Returns the set of vertices
        """
        pass

    @abstractmethod
    def edges(self) -> set:
        """
        Returns the set of edges as `Edge` objects
        """
        pass


class MutableGraph (Graph):
    """
    This is the interfaces for a mutable directed graph. Aside from the basic interfaces for getting the neighbours and
    testing if the graph contains an element, it also provides interfaces to add vertices and edges to the graph
    """
    @abstractmethod
    def add_vertex(self, item):
        """
        Adds a vertex
        :param item: Vertex to add
        :return:
        """
        pass

    @abstractmethod
    def add_edge(self, edge: Edge):
        """
        The edge to add
        :param edge: An `Edge` struct
        :return:
        """
        pass


class AdjListDiGraph (MutableGraph):
    """
    Implementation of a directed graph using adjacency list
    """
    def __init__(self):
        self.storage = dict()

    """
    {}
    """.format(Graph.get_neighbours.__doc__)
    def get_neighbours(self, item) -> list:
        if item not in self.storage:
            return None
        else:
            return self.storage[item]

    """
    {}
    """.format(MutableGraph.add_vertex.__doc__)
    def add_vertex(self, item):
        if item not in self.storage:
            self.storage[item] = set()

    """
    {}
    """.format(MutableGraph.add_edge.__doc__)
    def add_edge(self, edge: Edge):
        if edge.src not in self.storage or edge.destination not in self.storage:
            raise ValueError("Either the source ({}) or destination ({}) of the edge is not in the graph".format(
                edge.src,
                edge.destination
            ))
        self.storage[edge.src].add((edge.destination, edge.ppt))

    def __contains__(self, item):
        """
        {} 
        """.format(Graph.__contains__.__doc__)
        if type(item) == Edge:
            return item.src in self.storage and (item.destination, item.ppt) in item.storage[item.src]
        else:
            return item in self.storage

    def vertices(self) -> list:
        """
        {}
        """.format(Graph.vertices.__doc__)
        return set(self.storage.keys())

    def edges(self) -> set:
        """
        {}
        """.format(Graph.edges.__doc__)
        return set(flatten([[Edge(v, e[0], e[1]) for e in edges] for v, edges in self.storage.items()]))

    @staticmethod
    def from_json(json_str: str):
        data = json.loads(json_str)
        graph = AdjListDiGraph()
        for v in data.keys():
            graph.add_vertex(v)

        for v, edges in data.items():
            for destination, ppt in edges:
                graph.add_edge(Edge(v, destination, ppt))

        return graph


class AdjListUndirectedDiGraph (AdjListDiGraph):
    """
    Implementation of a directed graph using adjacency list.
    NOTE: For this, the vertices have to have the __gt__ operator implemented.
    NOTE: This does allow multiple edges with different weights to exist between nodes.
    """

    def add_edge(self, edge: Edge):
        if edge.src not in self.storage or edge.destination not in self.storage:
            raise ValueError("Either the source ({}) or destination ({}) of the edge is not in the graph".format(
                edge.src,
                edge.destination
            )
        )
        self.storage[edge.src].add((edge.destination, edge.ppt))
        self.storage[edge.destination].add((edge.src, edge.ppt))

    def edges(self) -> set:
        return set(
            flatten(
                [[Edge(v, e[0], e[1]) if e[0] > v else Edge(e[0], v, e[1]) for e in edges] for v, edges in self.storage.items()]
            )
        )

    @staticmethod
    def from_json(json_str: str):
        data = json.loads(json_str)
        graph = AdjListUndirectedDiGraph()
        for v in data.keys():
            graph.add_vertex(v)

        for v, edges in data.items():
            for destination, ppt in edges:
                graph.add_edge(Edge(v, destination, ppt))

        return graph

