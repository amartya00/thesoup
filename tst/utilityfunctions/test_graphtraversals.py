import dataclasses
import unittest

from typing import Any, List, Tuple

from thesoup.utilityclasses.graph import AdjListDiGraph, Graph
from thesoup.utilityfunctions.graphtraversals import bfs, dfs, dijkstra, shortest_path_dag, trace


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
        parents = dict()

        def _bfs_callback(info: Tuple[Any, Any, int]):
            u, v, w = info
            parents[v] = (u, w)

        bfs(graph, "A", _bfs_callback)
        self.assertEqual(
            {"A": (None, 0), "B": ("A", 1), "C": ("A", 1), "D": ("C", 2), "E": ("D", 3)},
            parents
        )
        parents.clear()

        bfs(graph, "B", _bfs_callback)
        self.assertEqual(
            {"B"}, set(parents.keys())
        )
        parents.clear()

        bfs(graph, "C", _bfs_callback)
        self.assertEqual(
            {"B", "C", "D", "E"}, set(parents.keys())
        )
        parents.clear()

        bfs(graph, "D", _bfs_callback)
        self.assertEqual(
            {"D", "E"}, set(parents.keys())
        )
        parents.clear()

        bfs(graph, "E", _bfs_callback)
        self.assertEqual(
            {"E"}, set(parents.keys())
        )
        parents.clear()

        bfs(graph, "Z", _bfs_callback)
        self.assertEqual(
            set(), set(parents.keys())
        )

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

    def test_trace(self):
        sample_graph_json = """
            {
                "A": ["B", "C"],
                "B": ["C", "D"],
                "C": ["D", "B"],
                "D": ["C"],
                "E": []
            }
            """
        graph = AdjListDiGraph.from_json(sample_graph_json)
        self.assertTrue(trace(graph, ["A", "C", "B", "D"]))
        self.assertFalse(trace(graph, ["A", "C", "B", "E"]))
        self.assertFalse(trace(graph, ["A", "D"]))
        self.assertTrue(trace(graph, []))
        self.assertFalse(trace(graph, ["A", "C", "B", "A"]))\


    def test_scrabble(self):
        @dataclasses.dataclass
        class MatrxElement:
            item: Any
            row: int
            col: int

            def __eq__(self, other):
                if type(other) == type(self):
                    return other.item == self.item and other.row == self.row and other.col == self.col
                else:
                    return other == self.item

        class Matrix (Graph):
            def __int__(self, matrix: List[List[Any]]):
                self._matrix = matrix[:]
                self._rows = len(matrix)
                self._cols = len(matrix[0]) if len(matrix) > 0 else 0

            def get_neighbours(self, item: MatrxElement) -> list:
                if type(item) != MatrxElement:
                    for r in range(self._rows):
                        for c in range(self._cols):
                            if self._matrix[r][c] == item:
                                row, col = r, c
                                return [self._matrix[r][c] for r, c in
                                        [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)] if
                                        0 <= r <= self._rows and 0 <= c <= self._cols]
                else:
                    row, col = item.row, item.col
                    return [self._matrix[r][c] for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)] if 0 <= r <= self._rows and 0 <= c <= self._cols]

            def __contains__(self, item):
                pass