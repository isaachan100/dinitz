import time

from flow import FlowAlg
from flow import FlowNetwork
from graph import Graph


"""
compute and plot the average time it takes to compute max flow over 100 trials for each n in [5, 10, ..., k]
graph_generator: function that generates a graph
graph_param: parameter for the graph generator
file_name: name of the output file
flow_alg: function that computes max flow
k: maximum number of vertices, defaults to 100
"""


def average_time_experiment(
    graph_generator, graph_param, file_name, graph_title, flow_algs, k=100
):
    results = [[] for _ in range(len(flow_algs))]

    for a, flow_alg in enumerate(flow_algs):
        for i in range(5, k, 5):
            total_time = 0
            iterations = 0
            non_zero_flows = 0

            for _ in range(250):
                graph = graph_generator(i, graph_param, 30)
                network = FlowNetwork(i, 0, i - 1)
                start_time = time.time()

                if flow_alg == FlowAlg.DINITZ:
                    f, iters = network.compute_max_flow_dinitz(graph)
                    iterations += iters
                elif flow_alg == FlowAlg.EDMONDS_KARP:
                    f, iters = network.compute_max_flow_edmonds_karp(graph)
                    iterations += iters

                end_time = time.time()
                total_time += end_time - start_time
                if sum(f[0].values()) > 0:
                    non_zero_flows += 1

            results[a].append([i, total_time / 100])
            print_experiment_results(
                total_time / 100, iterations / 100, non_zero_flows, i
            )

    Graph.plot_graph(
        [[x[0] for x in results[i]] for i in range(len(flow_algs))],
        [[x[1] for x in results[i]] for i in range(len(flow_algs))],
        flow_algs,
        "number of vertices",
        "average time in ms",
        graph_title,
        file_name,
    )


"""
compute and plot the average time it takes to compute max bipartite matching over 100 trials for each n in [5, 10, ..., k]
graph_generator: function that generates a bipartite graph
graph_param: parameter for the graph generator
file_name: name of the output file
flow_alg: function that computes max flow
k: maximum number of vertices, defaults to 100
"""


def bipartite_reduction_experiment(
    graph_generator,
    graph_param,
    file_name,
    graph_title,
    flow_algs,
    k=100,
):
    results = [[] for _ in range(len(flow_algs))]

    for a, flow_alg in enumerate(flow_algs):

        for i in range(5, k, 5):
            total_time = 0
            iterations = 0
            non_zero_flows = 0

            for _ in range(250):
                graph = graph_generator(i, graph_param)
                network = FlowNetwork(2 * i + 2, 0, 2 * i + 1)
                start_time = time.time()
                size, iters = network.compute_max_bipartite_matching_size(
                    graph, flow_alg
                )
                iterations += iters
                end_time = time.time()
                total_time += end_time - start_time
                if size > 0:
                    non_zero_flows += 1

            results[a].append([i, total_time / 100])
            print_experiment_results(
                total_time / 100, iterations / 100, non_zero_flows, i
            )

    Graph.plot_graph(
        [[x[0] for x in results[i]] for i in range(len(flow_algs))],
        [[x[1] for x in results[i]] for i in range(len(flow_algs))],
        flow_algs,
        "number of vertices in L",
        "average time in ms",
        graph_title,
        file_name,
    )


def print_experiment_results(average_time, average_iterations, non_zero_flows, n):
    print(
        "n =",
        n,
        "average time =",
        average_time,
        "non-zero flows =",
        non_zero_flows,
        "average iterations =",
        average_iterations,
    )


if __name__ == "__main__":
    print("starting experiment for renyi erdos graphs")
    average_time_experiment(
        Graph.generate_erdos_renyi_graph,
        0.1,
        "renyi_erdos.png",
        "average time to compute max flow renyi erdos",
        [FlowAlg.EDMONDS_KARP, FlowAlg.DINITZ],
        300,
    )

    print("starting experiment for barabasi albert graphs")
    average_time_experiment(
        Graph.generate_barabasi_albert_graph,
        15,
        "barabasi_albert.png",
        "average time to compute max flow barabasi albert",
        [FlowAlg.EDMONDS_KARP, FlowAlg.DINITZ],
        300,
    )

    print("starting experiment for bipartite matching")
    bipartite_reduction_experiment(
        Graph.generate_erdos_renyi_bipartite_graph,
        0.1,
        "bipartite.png",
        "average time to compute max bipartite matching size",
        [FlowAlg.EDMONDS_KARP, FlowAlg.DINITZ],
        200,
    )
