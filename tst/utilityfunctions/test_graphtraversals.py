import unittest

from thesoup.utilityclasses.graph import AdjListGraph
from thesoup.utilityfunctions.graphtraversals import bfs, dfs, dijkstra


class TestGraphTraversals (unittest.TestCase):
    def test_bfs(self):
        json_str = """
        {
            "A": [["B", 155], ["C", 123]],
            "B": [],
            "C": [["B", 98], ["D", 109]],
            "D": [["E", 98]],
            "E": []
        }
        """
        graph = AdjListGraph.from_json(json_str)
        self.assertEqual({"A", "B", "C", "D", "E"}, bfs(graph, "A"))
        self.assertEqual({"B"}, bfs(graph, "B"))
        self.assertEqual({"B", "C", "D", "E"}, bfs(graph, "C"))
        self.assertEqual({"D", "E"}, bfs(graph, "D"))
        self.assertEqual({"E"}, bfs(graph, "E"))
        self.assertEqual(set(), bfs(graph, "Z"))

    def test_dfs(self):
        json_str = """
        {
            "A": [["B", 155], ["C", 123]],
            "B": [],
            "C": [["B", 98], ["D", 109]],
            "D": [["E", 98]],
            "E": []
        }
        """
        graph = AdjListGraph.from_json(json_str)
        self.assertEqual({"A", "B", "C", "D", "E"}, dfs(graph, "A"))
        self.assertEqual({"B"}, dfs(graph, "B"))
        self.assertEqual({"B", "C", "D", "E"}, dfs(graph, "C"))
        self.assertEqual({"D", "E"}, dfs(graph, "D"))
        self.assertEqual({"E"}, dfs(graph, "E"))
        self.assertEqual(set(), dfs(graph, "Z"))

    def test_dijkstra(self):
        sample_graph_json = """
        {
            "A": [["B", 10], ["C", 2]],
            "B": [["D", 9]],
            "C": [["B", 3], ["D", 27]],
            "D": []
        }
        """
        graph = AdjListGraph.from_json(sample_graph_json)
        d, predecessors = dijkstra(graph, "A")
        self.assertEqual({"A": 0, "B": 5, "C": 2, "D": 14}, d)
        self.assertEqual({"A": None, "B": "C", "C": "A", "D": "B"}, predecessors)
