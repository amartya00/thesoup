class Edge:
    def __init__(self, src, destination, ppt):
        self.src = src
        self.destination = destination
        self.ppt = ppt

    def __hash__(self):
        hash("{}.{}.{}".format(self.src, self.destination, self.ppt))


class DiGraph:
    """
    This is the interface for a directed graph
    """
    def get_neighbours(self, item) -> list:
        """
        Returns the neighbours of a vertex
        :param item: Vertex whose neighbours to fetch
        :return:
        """
        pass

    def add_vertex(self, item):
        """
        Adds a vertex
        :param item: Vertex to add
        :return:
        """
        pass

    def add_edge(self, edge: Edge):
        """
        The edge to add
        :param edge: An `Edge` struct
        :return:
        """
        pass


class AdjListGraph (DiGraph):
    """
    Implementation of a directed graph using adjacensy list
    """
    def __init__(self):
        self.storage = dict()

    """
    {}
    """.format(DiGraph.get_neighbours.__doc__)
    def get_neighbours(self, item) -> list:
        if item not in self.storage:
            return None
        else:
            return self.storage[item]

    """
    {}
    """.format(DiGraph.add_vertex.__doc__)
    def add_vertex(self, item):
        if item not in self.storage:
            self.storage[item] = set()

    """
    {}
    """.format(DiGraph.add_edge.__doc__)
    def add_edge(self, edge: Edge):
        if edge.src not in self.storage or edge.destination not in self.storage:
            raise ValueError("Either the source ({}) or destination ({}) of the edge is not in the graph".format(
                edge.src,
                edge.destination
            ))
        self.storage[edge.src].add((edge.destination, edge.ppt))


print(help(AdjListGraph))