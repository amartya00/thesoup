import unittest

from thesoup.utilityfunctions.graphutils import topological_sort, kruskal
from thesoup.utilityclasses.graph import AdjListDiGraph, AdjListUndirectedDiGraph, Edge


class TestGraphUtils (unittest.TestCase):
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
        graph = AdjListDiGraph.from_json(sample_graph_json)
        vertices = dict(
            map(
                lambda elem: (elem[1], elem[0]),
                enumerate(topological_sort(graph))
            )
        )
        for edge in graph.edges():
            s, d = edge.src, edge.destination
            self.assertTrue(vertices[s] < vertices[d])

    def test_kruskal(self):
        sample_graph_json = """
        {
            "A": [["B", 9], ["C", 8], ["D", 4]],
            "B": [["D", 2]],
            "C": [["D", 3]],
            "D": []
        }
        """
        graph = AdjListUndirectedDiGraph.from_json(sample_graph_json)
        self.assertEqual({Edge("A", "D", 4), Edge("B", "D", 2), Edge("C", "D", 3)}, kruskal(graph))
