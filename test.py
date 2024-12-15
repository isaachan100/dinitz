import unittest

from typing import List

from flow import FlowNetwork


class TestFlowMethods(unittest.TestCase):
    def setUp(self):
        graph: List[dict[int]] = [
            {1: 2, 2: 3},
            {3: 1},
            {3: 2},
            {},
        ]

        self.flow_network = FlowNetwork(4, 0, 3)
        self.graph = graph

        graph1: List[dict[int]] = [
            {1: 1, 2: 1},
            {2: 1, 4: 1},
            {4: 1},
            {0: 2, 5: 2},
            {3: 2},
            {6: 2},
            {4: 2},
        ]

        self.flow_network1 = FlowNetwork(7, 0, 6)
        self.graph1 = graph1

        graph2: List[dict[int]] = [
            {1: 1, 2: 1, 3: 2},
            {2: 1, 4: 1},
            {4: 1},
            {4: 2, 5: 2},
            {6: 2},
            {6: 2},
            {},
        ]

        self.flow_network2 = FlowNetwork(7, 0, 6)
        self.graph2 = graph2

    def test_compute_advancing_graph(self):
        graph: List[dict[int]] = [{2: 3}, {0: 1}, {3: 4}, {1: 2}]

        advancing_graph = self.flow_network.compute_advancing_graph(graph)
        self.assertEqual(advancing_graph, [{2: 3}, {}, {3: 4}, {1: 2}])

        advancing_graph = self.flow_network.compute_advancing_graph(self.graph)
        self.assertEqual(advancing_graph, [{1: 2, 2: 3}, {3: 1}, {3: 2}, {}])

    def test_compute_blocking_flow(self):
        networks = [[self.flow_network, self.graph], [self.flow_network1, self.graph1]]

        res = [
            [{1: 1, 2: 2}, {3: 1}, {3: 2}, {}],
            [{1: 1, 2: 1}, {4: 1}, {4: 1}, {5: 2}, {3: 2}, {6: 2}, {}],
        ]

        for i, [network, graph] in enumerate(networks):
            self.assertEqual(network.compute_blocking_flow(graph), res[i])
            self.assertTrue(
                network.is_flow_feasible(graph, network.compute_blocking_flow(graph))
            )

    def test_compute_max_flow(self):
        networks = [[self.flow_network, self.graph], [self.flow_network2, self.graph2]]

        res = [
            [{1: 1, 2: 2}, {3: 1}, {3: 2}, {}],
            [
                {1: 1, 2: 1, 3: 2},
                {4: 1},
                {4: 1},
                {5: 2},
                {6: 2},
                {6: 2},
                {},
            ],
        ]

        for i, [network, graph] in enumerate(networks):
            self.assertEqual(network.compute_max_flow_dinitz(graph)[0], res[i])
            self.assertEqual(network.compute_max_flow_edmonds_karp(graph)[0], res[i])
            self.assertTrue(
                network.is_flow_feasible(
                    graph, network.compute_max_flow_dinitz(graph)[0]
                )
            )
            self.assertTrue(
                network.is_flow_feasible(
                    graph, network.compute_max_flow_edmonds_karp(graph)[0]
                )
            )


if __name__ == "__main__":
    unittest.main()
