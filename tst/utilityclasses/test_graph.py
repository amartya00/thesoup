import unittest

from thesoup.utilityclasses.graph import AdjListGraph, Edge


class TestEdge (unittest.TestCase):
    def test_edge_hash(self):
        e1 = Edge("A", "B", 123)
        e2 = Edge("A", "B", 124)
        e3 = Edge("A", "C", 123)
        e4 = Edge("A", "B", 123)
        self.assertEqual(hash("{}.{}.{}".format("A", "B", 123)), hash(e1))
        self.assertNotEqual(hash(e1), hash(e2))
        self.assertNotEqual(hash(e1), hash(e3))
        self.assertNotEqual(hash(e2), hash(e3))
        self.assertEqual(hash(e1), hash(e4))

    def test_equality(self):
        e1 = Edge("A", "B", 123)
        e2 = Edge("A", "B", 124)
        e3 = Edge("A", "C", 123)
        e4 = Edge("A", "B", 123)
        self.assertEqual(e1, e1)
        self.assertEqual(e1, e4)
        self.assertNotEqual(e1, e2)
        self.assertNotEqual(e1, e3)
        self.assertNotEqual(e2, e3)

    def test_set(self):
        e1 = Edge("A", "B", 123)
        e2 = Edge("A", "B", 124)
        e3 = Edge("A", "C", 123)
        e4 = Edge("A", "B", 123)
        my_set = {e1, e2, e3, e4}
        self.assertEqual(len(my_set), 3)

    def test_edge_str(self):
        e = Edge("A", "B", 100)
        self.assertEqual("{}.{}.{}".format("A", "B", 100), str(e))


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
        self.assertEqual({"A", "B", "C"}, g.vertices())

        expected_edge_set = {Edge("A", "B", 55), Edge("A", "C", 100), Edge("C", "B", 123)}
        self.assertEqual(expected_edge_set, g.edges())

    def test_exception_on_invalid_edge(self):
        g = AdjListGraph()
        with self.assertRaises(ValueError):
            g.add_edge(Edge("A", "B", 28))

    def test_json_initializer(self):
        json_str = """
        {
            "A": [["B", 155], ["C", 123]],
            "B": [],
            "C": [["B", 98]]
        }
        """
        g = AdjListGraph.from_json(json_str)
        self.assertEqual({("B", 155), ("C", 123)}, g.get_neighbours("A"))
        self.assertEqual({("B", 98)}, g.get_neighbours("C"))
        self.assertEqual(set(), g.get_neighbours("B"))
        self.assertEqual({"A", "B", "C"}, g.vertices())

        expected_edge_set = {Edge("A", "B", 155), Edge("A", "C", 123), Edge("C", "B", 98)}
        self.assertEqual(expected_edge_set, g.edges())
