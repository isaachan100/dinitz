import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")
import random

from typing import List


class Graph:
    def __init__(self):
        return

    """
    generates a random Erdos-Renyi graph with n vertices and edge probability p in (0, 1)
    each edge has capacity uniformly at random in [1, c]
    """

    def generate_erdos_renyi_graph(n: int, p: float, c: int):
        graph = [{} for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if random.random() < p:
                    graph[i][j] = random.uniform(1, c)

        return graph

    def generate_barabasi_albert_graph(n: int, m: int, c: int):
        graph = [{} for _ in range(n)]
        degrees = [0 for _ in range(n)]

        # manually create an edge at the beginning
        graph[0][1] = random.uniform(1, c)
        degrees[0] = 1
        degrees[1] = 1

        for i in range(2, n):
            nodes = list(range(i))
            selected_nodes = set(random.choices(nodes, weights=degrees[:i], k=m))

            for node in selected_nodes:
                degrees[node] += 1
                graph[node][i] = random.uniform(1, c)

            degrees[i] = len(selected_nodes)

        return graph

    def plot_graph(x: List[int], y: List[float], file_name: str):
        plt.plot(x, y)
        plt.savefig(file_name)
