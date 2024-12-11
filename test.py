import unittest

from typing import List

from flow import FlowNetwork

class TestFlowMethods(unittest.TestCase):
    def setUp(self):
        capacities : List[List[int]] = [
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [3, 0, 0, 0],
            [0, 1, 2, 0]
        ]

        self.flow_network = FlowNetwork(4, capacities, 0, 3)


    def test_initialize_flow(self):
        with self.assertRaises(ValueError):
            FlowNetwork(2, [[1, 2], [3, 4], [0, 0]], 0, 1)

    def test_flow_feasible(self):
        flow : List[List[int]] = [
            [0, -1, -2, 0],
            [1, 0, 0, -1],
            [2, 0, 0, -2],
            [0, 1, 2, 0]
        ]

        self.assertTrue(self.flow_network.isFlowFeasible(flow))

        flow[1][0] = 0
        self.assertFalse(self.flow_network.isFlowFeasible(flow))

        flow[1][0] = 1
        flow[0][2] = 3
        flow[2][0] = -3
        self.assertFalse(self.flow_network.isFlowFeasible(flow))

        flow[2][3] = 3
        flow[3][2] = -3
        self.assertFalse(self.flow_network.isFlowFeasible(flow))


if __name__ == '__main__':
    unittest.main()