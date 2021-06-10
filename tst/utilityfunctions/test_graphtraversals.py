import unittest

from thesoup.utilityclasses.graph import AdjListDiGraph
from thesoup.utilityfunctions.graphtraversals import bfs, dfs, dijkstra, shortest_path_dag
from thesoup.utilityfunctions.collectionutils import flatten


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
        graph = AdjListDiGraph.from_json(json_str)
        self.assertEqual({0: {"A"}, 1: {"B", "C"}, 2: {"D"}, 3: {"E"}}, bfs(graph, "A"))
        self.assertEqual({"B"}, set(flatten(bfs(graph, "B").values())))
        self.assertEqual({"B", "C", "D", "E"}, set(flatten(bfs(graph, "C").values())))
        self.assertEqual({"D", "E"}, set(flatten(bfs(graph, "D").values())))
        self.assertEqual({"E"}, set(flatten(bfs(graph, "E").values())))
        self.assertEqual(set(), set(flatten(bfs(graph, "Z").values())))

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
        graph = AdjListDiGraph.from_json(json_str)
        parents = dfs(graph, "A")
        self.assertTrue(parents["A"] is None)
        self.assertTrue(parents["B"] == "A" or parents["B"] == "C")
        self.assertTrue(parents["C"] == "A")
        self.assertTrue(parents["D"] == "C")
        self.assertTrue(parents["E"] == "D")

        self.assertEqual({"B"}, set(dfs(graph, "B").keys()))
        self.assertEqual({"B", "C", "D", "E"}, set(dfs(graph, "C").keys()))
        self.assertEqual({"D", "E"}, set(dfs(graph, "D").keys()))
        self.assertEqual({"E"}, set(dfs(graph, "E").keys()))
        self.assertEqual(set(), set(dfs(graph, "Z").keys()))

    def test_dijkstra(self):
        sample_graph_json = """
        {
            "A": [["B", 10], ["C", 2]],
            "B": [["D", 9]],
            "C": [["B", 3], ["D", 27]],
            "D": []
        }
        """
        graph = AdjListDiGraph.from_json(sample_graph_json)
        d, predecessors = dijkstra(graph, "A")
        self.assertEqual({"A": 0, "B": 5, "C": 2, "D": 14}, d)
        self.assertEqual({"A": None, "B": "C", "C": "A", "D": "B"}, predecessors)

    def test_shortest_path_dag(self):
        sample_graph_json = """
        {
            "A": [["B", 1], ["C", 12]],
            "B": [["C", 3], ["D", 7]],
            "C": [["D", 1]],
            "D": []
        }
        """
        graph = AdjListDiGraph.from_json(sample_graph_json)
        sp, predecessors = shortest_path_dag(graph, "A", "D")
        self.assertEqual(5, sp)
        self.assertEqual(
            {
                "A": None,
                "B": "A",
                "C": "B",
                "D": "C"
            },
            predecessors
        )

    def test_sp_DAG_on_non_existent_nodes(self):
        sample_graph_json = """
                {
                    "A": [["B", 1], ["C", 12]],
                    "B": [["C", 3], ["D", 7]],
                    "C": [["D", 1]],
                    "D": []
                }
                """
        graph = AdjListDiGraph.from_json(sample_graph_json)
        sp, predecessors = shortest_path_dag(graph, "A", "Z")
        self.assertEqual(float("inf"), sp)
        self.assertEqual(
            {
                "A": None
            },
            predecessors
        )
        sp1, predecessors1 = shortest_path_dag(graph, "Z", "Z")
        self.assertEqual(0, sp1)
        self.assertEqual(
            {
                "Z": None
            },
            predecessors1
        )
        sp1, predecessors1 = shortest_path_dag(graph, "Z", "C")
        self.assertEqual(float("inf"), sp1)
        self.assertEqual(
            {
                "Z": None
            },
            predecessors1
        )

    def test_unreachable_dag_sp(self):
        sample_graph_json = """
            {
                "A": [["B", 1], ["C", 12]],
                "B": [["C", 3], ["D", 7]],
                "C": [["D", 1]],
                "D": [],
                "E": []
            }
            """
        graph = AdjListDiGraph.from_json(sample_graph_json)
        sp, predecessors = shortest_path_dag(graph, "A", "E")
        self.assertEqual(float("inf"), sp)
        self.assertEqual(
            {
                "A": None
            },
            predecessors
        )
