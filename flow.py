import copy

from typing import List


class FlowNetwork:
    def __init__(
        self, num_vertices: int, capacities: List[List[int]], source: int, dest: int
    ):
        if len(capacities) != num_vertices or any(
            len(row) != num_vertices for row in capacities
        ):
            raise ValueError(
                "Capacities must be a square matrix of size num_vertices x num_vertices"
            )

        self.capacities = capacities
        self.dest = dest
        self.num_vertices = num_vertices
        self.source = source

    def is_flow_feasible(self, flow: List[List[int]]) -> bool:
        if len(flow) != self.num_vertices or any(
            len(row) != self.num_vertices for row in flow
        ):
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

    def compute_max_flow(self):
        f = [[0 for _ in range(self.num_vertices)] for _ in range(self.num_vertices)]
        residual_graph = copy.deepcopy(self.capacities)

        while self.contains_st_path(residual_graph):
            blocking_flow = self.compute_blocking_flow(residual_graph)
            f = self.sum_matrices(f, blocking_flow)
            residual_graph = self.subtract_matrices(residual_graph, blocking_flow)

        return f

    """
    takes a graph G represented by a matrix of capacities
    returns a blocking flow specified by Algorithm 3 from section 4.3 of 6820 Flow lecture notes
    """

    def compute_blocking_flow(self, graph: List[List[int]]) -> List[List[int]]:
        h = [[0 for _ in range(self.num_vertices)] for _ in range(self.num_vertices)]

        advancing_graph, residual_capacities = self.compute_advancing_graph(graph)

        stack = [self.source]

        while len(stack) != 0:
            u = stack[-1]

            if u == self.dest:
                delta = min(
                    [
                        residual_capacities[stack[i]][stack[i + 1]]
                        for i in range(len(stack) - 1)
                    ]
                )
                for i in range(len(stack) - 1):
                    h[stack[i]][stack[i + 1]] += delta
                    h[stack[i + 1]][stack[i]] -= delta
                    residual_capacities[stack[i]][stack[i + 1]] -= delta
                    residual_capacities[stack[i + 1]][stack[i]] += delta

                edges_to_delete = []
                for i in range(len(stack) - 1):
                    if residual_capacities[stack[i]][stack[i + 1]] == 0:
                        edges_to_delete.append((stack[i], stack[i + 1]))

                for i, j in edges_to_delete:
                    advancing_graph[i].remove(j)

                a = edges_to_delete[0][0]
                while stack[-1] != a:
                    stack.pop()
            elif len(advancing_graph[u]) != 0:
                stack.append(advancing_graph[u][0])
            else:
                # TODO: can probably make this faster with reverse adjacency list
                for v in range(self.num_vertices):
                    if u in advancing_graph[v]:
                        advancing_graph[v].remove(u)
                stack.pop()

        return h

    """
    takes a graph G in matrix form and returns a graph composed of advancing edges of G in adjacency list form
    also returns the residual capacities of the advancing edges
    """

    def compute_advancing_graph(self, capacities: List[List[int]]):
        advancing_graph = [[] for _ in range(self.num_vertices)]
        residual_capacities = [
            [0 for _ in range(self.num_vertices)] for _ in range(self.num_vertices)
        ]

        stack = [self.source]
        visited = {self.source: 0}

        while len(stack) != 0:
            node = stack.pop()
            level = visited[node]

            for i in range(self.num_vertices):
                if capacities[node][i] > 0 and (i not in visited or visited[i] > level):
                    advancing_graph[node].append(i)
                    residual_capacities[node][i] = capacities[node][i]
                    stack.append(i)
                    if i not in visited:
                        visited[i] = level + 1

        return advancing_graph, residual_capacities

    def sum_matrices(self, matrix1: List[List[int]], matrix2: List[List[int]]):
        return [
            [matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))]
            for i in range(len(matrix1))
        ]

    def subtract_matrices(self, matrix1: List[List[int]], matrix2: List[List[int]]):
        return [
            [matrix1[i][j] - matrix2[i][j] for j in range(len(matrix1[0]))]
            for i in range(len(matrix1))
        ]

    def contains_st_path(self, residual_graph: List[List[int]]) -> bool:
        visited = set()
        visited.add(self.source)
        stack = [self.source]

        while len(stack) != 0:
            u = stack.pop()
            for v in range(self.num_vertices):
                if residual_graph[u][v] > 0 and v not in visited:
                    if v == self.dest:
                        return True
                    stack.append(v)
                    visited.add(v)

        return False
