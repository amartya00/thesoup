import unittest

from thesoup.utilityfunctions.graphutils import topological_sort
from thesoup.utilityclasses.graph import AdjListGraph


class TestTopologicalSort (unittest.TestCase):
    def test_topological_sort(self):
        sample_graph_json = """
        {
            "A": [["C", 1]],
            "B": [["C", 2], ["D", 10]],
            "C": [["E", 17]],
            "D": [["F", 8]],
            "E": [["F", 32], ["H", 3]],
            "F": [["G", 11]],
            "G": [],
            "H": []
        }
        """
        graph = AdjListGraph.from_json(sample_graph_json)
        vertices = dict(
            map(
                lambda elem: (elem[1], elem[0]),
                enumerate(topological_sort(graph))
            )
        )
        for edge in graph.edges():
            s, d = edge.src, edge.destination
            self.assertTrue(vertices[s] < vertices[d])
