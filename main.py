import time

from flow import FlowNetwork
from graph import Graph

"""
compute and plot the average time it takes to compute max flow over 100 trials for each n in [5, 10, ..., 95]
graph_generator: function that generates a graph
graph_param: parameter for the graph generator
file_name: name of the output file
"""


def average_time_experiment(graph_generator, graph_param, file_name):
    results = []

    for i in range(5, 100, 5):
        total_time = 0
        non_zero_flows = 0

        for _ in range(100):
            graph = graph_generator(i, graph_param, 30)
            network = FlowNetwork(i, 0, i - 1)
            start_time = time.time()
            f = network.compute_max_flow_dinitz(graph)
            end_time = time.time()
            total_time += end_time - start_time
            if sum(f[0].values()) > 0:
                non_zero_flows += 1

        average_time = total_time / 100
        results.append([i, average_time])
        print(
            "n =", i, "average time =", average_time, "non-zero flows =", non_zero_flows
        )

    Graph.plot_graph([x[0] for x in results], [x[1] for x in results], file_name)


if __name__ == "__main__":
    # average_time_experiment(Graph.generate_erdos_renyi_graph, .1, "erdos_renyi.png")
    average_time_experiment(
        Graph.generate_barabasi_albert_graph, 15, "barabasi_albert.png"
    )
