import matplotlib.pyplot as plt
import random

from typing import List


class Graph:
    def __init__(self):
        return

    """
    generates a random Erdos-Renyi graph with n vertices and edge probability p
    each edge has capacity uniformly at random in [1, c]
    """

    def generate_erdos_renyi_graph(n: int, p: float, c: int) -> List[List[int]]:
        if p < 0 or p > 1:
            raise ValueError("p must be in the range [0, 1]")

        graph = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if random.random() < p:
                    graph[i][j] = random.uniform(1, c)

        return graph
