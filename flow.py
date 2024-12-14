import copy

from collections import defaultdict
from typing import List


class FlowNetwork:
    def __init__(self, num_vertices: int, source: int, dest: int):
        self.dest = dest
        self.num_vertices = num_vertices
        self.source = source

    def is_flow_feasible(self, graph, flow) -> bool:
        # first check capacity constraint
        for i in range(len(flow)):
            for k in flow[i].keys():
                if (
                    k not in graph[i].keys()
                    or flow[i][k] > graph[i][k]
                    or flow[i][k] < 0
                ):
                    print(flow, graph, i, k)
                    return False

        # second check flow conservation
        for i in range(len(graph)):
            if i == self.source or i == self.dest:
                continue

            in_flow = sum([flow[j][i] for j in range(len(flow))])
            out_flow = sum([flow[i][j] for j in flow[i].keys()])

            if in_flow != out_flow:
                return False

        return True

    def compute_max_flow_dinitz(self, graph: List[dict[int]]):
        n = len(graph)
        f = [defaultdict(int) for i in range(n)]
        residual_graph = self.construct_residual_graph(graph)

        while self.contains_st_path(residual_graph):
            blocking_flow = self.compute_blocking_flow(residual_graph)
            self.sum_flows(f, blocking_flow)
            self.update_residual_graph(residual_graph, blocking_flow)

        return f

    """
    takes a graph G represented by a matrix of capacities
    returns a blocking flow specified by Algorithm 3 from section 4.3 of 6820 Flow lecture notes
    """

    def compute_blocking_flow(self, graph: List[dict[int]]) -> List[List[int]]:
        h = [defaultdict(int) for i in range(len(graph))]

        advancing_graph = self.compute_advancing_graph(graph)

        stack = [self.source]

        while len(stack) != 0:
            u = stack[-1]

            if u == self.dest:
                delta = min(
                    [
                        advancing_graph[stack[i]][stack[i + 1]]
                        for i in range(len(stack) - 1)
                    ]
                )
                for i in range(len(stack) - 1):
                    h[stack[i]][stack[i + 1]] += delta
                    advancing_graph[stack[i]][stack[i + 1]] -= delta

                edges_to_delete = []
                for i in range(len(stack) - 1):
                    if advancing_graph[stack[i]][stack[i + 1]] == 0:
                        edges_to_delete.append((stack[i], stack[i + 1]))

                for i, j in edges_to_delete:
                    del advancing_graph[i][j]

                a = edges_to_delete[0][0]
                while stack[-1] != a:
                    stack.pop()
            elif len(advancing_graph[u]) != 0:
                keys = advancing_graph[u].keys()
                for key in keys:
                    stack.append(key)
                    break
            else:
                # TODO: can probably make this faster with reverse adjacency list
                for v in range(self.num_vertices):
                    if u in advancing_graph[v]:
                        del advancing_graph[v][u]
                stack.pop()

        return h

    """
    takes a graph G and returns a graph composed of advancing edges of G in adjacency list form
    """

    def compute_advancing_graph(self, graph: List[dict[int]]) -> List[dict[int]]:
        advancing_graph = [{} for _ in range(self.num_vertices)]

        stack = [self.source]
        visited = {self.source: 0}

        while len(stack) != 0:
            node = stack.pop()
            level = visited[node]

            for i, c in graph[node].items():
                if c > 0 and (i not in visited or visited[i] > level):
                    advancing_graph[node][i] = c
                    stack.append(i)
                    if i not in visited:
                        visited[i] = level + 1

        return advancing_graph

    """
    adds flow h to flow f
    """

    def sum_flows(self, f, h):
        for i in range(len(h)):
            for k in h[i].keys():
                f[i][k] += h[i][k]

    def construct_residual_graph(self, graph):
        residual_graph = [defaultdict(int) for i in range(len(graph))]

        for i in range(len(graph)):
            for j in graph[i].keys():
                residual_graph[i][j] = graph[i][j]

        return residual_graph

    def update_residual_graph(self, residual_graph, flow):
        for i in range(len(flow)):
            for k in flow[i].keys():
                residual_graph[i][k] -= flow[i][k]
                residual_graph[k][i] += flow[i][k]

    def contains_st_path(self, residual_graph) -> bool:
        visited = set()
        visited.add(self.source)
        stack = [self.source]

        while len(stack) != 0:
            u = stack.pop()
            for v, c in residual_graph[u].items():
                if c > 0 and v not in visited:
                    if v == self.dest:
                        return True
                    stack.append(v)
                    visited.add(v)

        return False
