from collections import defaultdict
from enum import Enum
from typing import List
from queue import Queue


class FlowAlg(Enum):
    DINITZ = 1
    EDMONDS_KARP = 2


class FlowNetwork:
    def __init__(self, num_vertices: int, source: int, dest: int):
        self.dest = dest
        self.num_vertices = num_vertices
        self.source = source

    """
    returns whether a flow is feasible based on Tardos and Kleinberg flows
    """

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

    """
    compute max flow using Dinitz algorithm
    """

    def compute_max_flow_dinitz(self, graph: List[dict[int]]):
        n = len(graph)
        f = [defaultdict(int) for i in range(n)]
        residual_graph = self.construct_residual_graph(graph)

        iterations = 0

        while self.contains_st_path(residual_graph):
            iterations += 1
            blocking_flow = self.compute_blocking_flow(residual_graph)
            self.sum_flows(f, blocking_flow)
            self.update_residual_graph(residual_graph, blocking_flow)

        return f, iterations

    """
    compute max flow using Edmonds-Karp algorithm
    """

    def compute_max_flow_edmonds_karp(self, graph: List[dict[int]]):
        n = len(graph)
        f = [defaultdict(int) for _ in range(n)]
        residual_graph = self.construct_residual_graph(graph)

        iterations = 0

        while self.contains_st_path(residual_graph):
            iterations += 1
            path_flow = self.compute_shortest_path_flow(residual_graph)
            self.sum_flows(f, path_flow)
            self.update_residual_graph(residual_graph, path_flow)

        return f, iterations

    """
    graph should have 2n vertices, L = [1, ..., n] and R = [n + 1, 2n]
    """

    """
    computes the maximum size of a bipartite matching in a bipartite graph
    """

    def compute_max_bipartite_matching_size(
        self, graph: List[dict[int]], flow_alg: FlowAlg
    ) -> int:
        n = len(graph) // 2
        f = [defaultdict(int) for _ in range(2 * n + 2)]

        # add edges for source = 0 and dest = 2n + 1
        graph.insert(0, dict([(i, 1) for i in range(1, n + 1)]))
        for i in range(n + 1, 2 * n + 1):
            graph[i][2 * n + 1] = 1
        graph.append({})

        if flow_alg == FlowAlg.DINITZ:
            f, iterations = self.compute_max_flow_dinitz(graph)
            return sum([f[0][i] for i in range(1, n + 1)]), iterations
        elif flow_alg == FlowAlg.EDMONDS_KARP:
            f, iterations = self.compute_max_flow_edmonds_karp(graph)
            return sum([f[0][i] for i in range(1, n + 1)]), iterations

    """
    takes a graph G represented by a matrix of capacities
    returns a blocking flow specified by Algorithm 3 from section 4.3 of 6820 Flow lecture notes
    """

    def compute_blocking_flow(self, graph: List[dict[int]]) -> List[dict[int]]:
        h = [defaultdict(int) for _ in range(len(graph))]

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

        # compute level graph first
        level = [-1] * self.num_vertices
        level[self.source] = 0
        queue = Queue()
        queue.put(self.source)

        while not queue.empty():
            u = queue.get(0)
            for v, c in graph[u].items():
                if c > 0 and level[v] == -1:
                    level[v] = level[u] + 1
                    queue.put(v)

        # iterate through edges and add advancing edges to advancing_graph
        for u in range(self.num_vertices):
            for v, c in graph[u].items():
                if c > 0 and level[v] > level[u]:
                    advancing_graph[u][v] = c

        return advancing_graph

    """
    adds flow h to flow f
    """

    def sum_flows(self, f, h):
        for i in range(len(h)):
            for k in h[i].keys():
                f[i][k] += h[i][k]

    """
    constructs the residual graph of [graph]
    """

    def construct_residual_graph(self, graph):
        residual_graph = [defaultdict(int) for i in range(len(graph))]

        for i in range(len(graph)):
            for j in graph[i].keys():
                residual_graph[i][j] = graph[i][j]

        return residual_graph

    """
    updates [residual_graph] with [flow]
    """

    def update_residual_graph(self, residual_graph, flow):
        for i in range(len(flow)):
            for k in flow[i].keys():
                residual_graph[i][k] -= flow[i][k]
                residual_graph[k][i] += flow[i][k]

    """
    returns true if [residual_graph] contains a path from source to dest
    """

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

    """
    using BFS, computes the shortest path from source to dest in [residual_graph]
    note: this function assumes such a path exists
    """

    def compute_shortest_path_flow(self, residual_graph):
        visited = set()
        visited.add(self.source)
        queue = Queue()
        queue.put(self.source)
        parent = {self.source: None}

        while not queue.empty():
            u = queue.get()
            for v, c in residual_graph[u].items():
                if c > 0 and v not in visited:
                    queue.put(v)
                    visited.add(v)
                    parent[v] = u

        path = []
        v = self.dest
        while v is not None:
            path.append(v)
            v = parent[v]

        path.reverse()

        min_capacity = min(
            [residual_graph[path[i]][path[i + 1]] for i in range(len(path) - 1)]
        )
        path_flow = [defaultdict(int) for i in range(len(residual_graph))]
        for i in range(len(path) - 1):
            path_flow[path[i]][path[i + 1]] = min_capacity

        return path_flow
