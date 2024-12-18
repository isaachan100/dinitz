import matplotlib
import matplotlib.pyplot as plt
import random

from typing import List

matplotlib.use("Agg")


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

    """
    generates a random Erdos-Renyi bipartite graph with n vertices and edge probability p in (0, 1)
    """

    def generate_erdos_renyi_bipartite_graph(n: int, p: float):
        graph = [{} for _ in range(1, 2 * n + 1)]

        for i in range(1, n + 1):
            for j in range(n + 1, 2 * n + 1):
                if random.random() < p:
                    graph[i][j] = 1

        return graph

    """
    generates a random Barabasi-Albert graph with n vertices and m edges to attach for each new node
    each edge has capacity uniformly at random in [1, c]
    """

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

    """
    plot graph with given parameters
    """

    def plot_graph(
        x: List[List[int]],
        y: List[List[float]],
        algs: List[str],
        x_label,
        y_label,
        title,
        file_name,
    ):
        plt.figure()

        for i in range(len(x)):
            plt.plot(x[i], y[i], label=algs[i])

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        if len(algs) > 1:
            plt.legend()
        plt.savefig(f"./plots/{file_name}")
