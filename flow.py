from typing import List

class FlowNetwork:
    def __init__(self, num_vertices : int, capacities : List[List[int]], source: int, dest: int):
        if len(capacities) != num_vertices or any(len(row) != num_vertices for row in capacities):
            raise ValueError("Capacities must be a square matrix of size num_vertices x num_vertices")
        
        self.capacities = capacities
        self.dest = dest
        self.num_vertices = num_vertices
        self.source = source

    def isFlowFeasible(self, flow : List[List[int]]) -> bool:
        if len(flow) != self.num_vertices or any(len(row) != self.num_vertices for row in flow):
            return False
        
        # first check skew-symmetry
        for i in range(self.num_vertices):
            for j in range(i):
                if flow[i][j] + flow[j][i] != 0:
                    return False
        
                
        # second check flow conservation
        for i in range(self.num_vertices):
            if i == self.source or i == self.dest:
                continue
            if sum(flow[i][j] for j in range(self.num_vertices)) != 0:
                return False

        # third check capacity constraint
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if flow[i][j] > self.capacities[i][j]:
                    return False
        
        return True