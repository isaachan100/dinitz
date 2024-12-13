import unittest

from typing import List

from flow import FlowNetwork

class TestFlowMethods(unittest.TestCase):
    def setUp(self):
        capacities : List[List[int]] = [
            [0, 2, 3, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 2],
            [0, 0, 0, 0]
        ]

        self.flow_network = FlowNetwork(4, capacities, 0, 3)

        capacities1 : List[List[int]] = [
            [0, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [2, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 2, 0, 0]
        ]

        self.flow_network1 = FlowNetwork(7, capacities1, 0, 6)

        capacities2 : List[List[int]] = [
            [0, 1, 1, 2, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0]
        ]

        self.flow_network2 = FlowNetwork(7, capacities2, 0, 6)

    def test_initialize_flow(self):
        with self.assertRaises(ValueError):
            FlowNetwork(2, [[1, 2], [3, 4], [0, 0]], 0, 1)

    def test_flow_feasible(self):
        flow : List[List[int]] = [
            [0, 1, 2, 0],
            [-1, 0, 0, 1],
            [-2, 0, 0, 2],
            [0, -1, -2, 0]
        ]

        self.assertTrue(self.flow_network.is_flow_feasible(flow))

        # check skew-symmetry
        flow[1][0] = 0
        self.assertFalse(self.flow_network.is_flow_feasible(flow))

        # check flow conservation
        flow[1][0] = 1
        flow[0][2] = 3
        flow[2][0] = -3
        self.assertFalse(self.flow_network.is_flow_feasible(flow))

        # check capacity constraint
        flow[2][3] = 3
        flow[3][2] = -3
        self.assertFalse(self.flow_network.is_flow_feasible(flow))

    def test_compute_advancing_graph(self):
        capacities : List[List[int]] = [
            [0, 0, 3, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 4],
            [0, 2, 0, 0]
        ]

        advancing_graph, residual_capacities = self.flow_network.compute_advancing_graph(capacities)
        self.assertEqual(advancing_graph, [[2], [], [3], [1]])
        self.assertEqual(residual_capacities, [
            [0, 0, 3, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 4],
            [0, 2, 0, 0]
        ])

        advancing_graph, residual_capacities = self.flow_network.compute_advancing_graph(self.flow_network.capacities)
        self.assertEqual(advancing_graph, [[1, 2], [3], [3], []])
        self.assertEqual(residual_capacities, [
            [0, 2, 3, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 2],
            [0, 0, 0, 0]
        ])
    
    def test_compute_blocking_flow(self):
        networks = [
            self.flow_network,
            self.flow_network1
        ]
        
        res = [
            [
                [0, 1, 2, 0],
                [-1, 0, 0, 1],
                [-2, 0, 0, 2],
                [0, -1, -2, 0]
            ],
            [
                [0, 1, 1, 0, 0, 0, 0], 
                [-1, 0, 0, 0, 1, 0, 0], 
                [-1, 0, 0, 0, 1, 0, 0], 
                [0, 0, 0, 0, -2, 2, 0], 
                [0, -1, -1, 2, 0, 0, 0], 
                [0, 0, 0, -2, 0, 0, 2], 
                [0, 0, 0, 0, 0, -2, 0]
            ]
        ]

        for i, network in enumerate(networks):
            self.assertEqual(network.compute_blocking_flow(network.capacities), res[i])
            self.assertTrue(network.is_flow_feasible(network.compute_blocking_flow(network.capacities)))
    
    def test_compute_max_flow(self):
        networks = [
            self.flow_network,
            self.flow_network2
        ]

        res = [
            [
                [0, 1, 2, 0],
                [-1, 0, 0, 1],
                [-2, 0, 0, 2],
                [0, -1, -2, 0]
            ],
            [
                [0, 1, 1, 2, 0, 0, 0], 
                [-1, 0, 0, 0, 1, 0, 0], 
                [-1, 0, 0, 0, 1, 0, 0], 
                [-2, 0, 0, 0, 0, 2, 0], 
                [0, -1, -1, 0, 0, 0, 2], 
                [0, 0, 0, -2, 0, 0, 2], 
                [0, 0, 0, 0, -2, -2, 0]
            ]
        ]

        for i, network in enumerate(networks):
            self.assertEqual(network.compute_max_flow(), res[i])
            self.assertTrue(network.is_flow_feasible(network.compute_max_flow()))
            

if __name__ == '__main__':
    unittest.main()