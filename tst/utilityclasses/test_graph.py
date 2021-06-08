import unittest

from thesoup.utilityclasses.graph import AdjListGraph, Edge


class TestGraph (unittest.TestCase):
    def test_graph_happy_case(self):
        g = AdjListGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_vertex("C")
        g.add_edge(Edge("A", "B", 55))
        g.add_edge(Edge("A", "C", 100))
        g.add_edge(Edge("C", "B", 123))

        self.assertEqual({("B", 55), ("C", 100)}, g.get_neighbours("A"))
        self.assertEqual({("B", 123)}, g.get_neighbours("C"))

    def test_exception_on_invalid_edge(self):
        g = AdjListGraph()
        with self.assertRaises(ValueError):
            g.add_edge(Edge("A", "B", 28))
