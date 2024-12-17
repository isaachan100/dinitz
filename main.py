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
    graph_generator, graph_param, file_name, graph_title, flow_algs, graph_type, k=100
):
    results = [[] for _ in range(len(flow_algs))]
    iteration_results = [[] for _ in range(len(flow_algs))]

    for a, flow_alg in enumerate(flow_algs):
        for i in range(5, k, 5):
            total_time = 0
            iterations = 0
            non_zero_flows = 0

            rounds = 50

            for _ in range(rounds):
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

            results[a].append([i, total_time / rounds])
            iteration_results[a].append([i, iterations / rounds])
            print_experiment_results(
                total_time / rounds, iterations / rounds, non_zero_flows, i
            )

    Graph.plot_graph(
        [[x[0] for x in results[i]] for i in range(len(flow_algs))],
        [[x[1] for x in results[i]] for i in range(len(flow_algs))],
        [flow_alg.value for flow_alg in flow_algs],
        "number of vertices",
        "average time in seconds",
        graph_title,
        file_name,
    )
    Graph.plot_graph(
        [[x[0] for x in results[0]]],
        [[results[0][i][1] / results[1][i][1] for i in range(len(results[0]))]],
        ["ratio"],
        "number of vertices",
        "ratio of time for Edmonds-Karp to Dinitz",
        "ratio of time for " + graph_type,
        "ratio_" + file_name,
    )
    Graph.plot_graph(
        [[x[0] for x in iteration_results[i]] for i in range(len(flow_algs))],
        [[x[1] for x in iteration_results[i]] for i in range(len(flow_algs))],
        [flow_alg.value for flow_alg in flow_algs],
        "number of vertices",
        "average iterations",
        "average number of iterations for " + graph_type,
        "iterations_" + file_name,
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
    iteration_results = [[] for _ in range(len(flow_algs))]

    for a, flow_alg in enumerate(flow_algs):

        for i in range(5, k, 5):
            total_time = 0
            iterations = 0
            non_zero_flows = 0

            rounds = 50

            for _ in range(rounds):
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

            results[a].append([i, total_time / rounds])
            iteration_results[a].append([i, iterations / rounds])
            print_experiment_results(
                total_time / rounds, iterations / rounds, non_zero_flows, i
            )

    Graph.plot_graph(
        [[x[0] for x in results[i]] for i in range(len(flow_algs))],
        [[x[1] for x in results[i]] for i in range(len(flow_algs))],
        [flow_alg.value for flow_alg in flow_algs],
        "number of vertices in L",
        "average time in seconds",
        graph_title,
        file_name,
    )
    Graph.plot_graph(
        [[x[0] for x in results[0]]],
        [[results[0][i][1] / results[1][i][1] for i in range(len(results[0]))]],
        ["ratio"],
        "number of vertices in L",
        "ratio of time for Edmonds-Karp to Dinitz",
        "ratio of time for bipartite matching",
        "ratio_" + file_name,
    )
    Graph.plot_graph(
        [[x[0] for x in iteration_results[i]] for i in range(len(flow_algs))],
        [[x[1] for x in iteration_results[i]] for i in range(len(flow_algs))],
        [flow_alg.value for flow_alg in flow_algs],
        "number of vertices in L",
        "average iterations",
        "average number of iterations for bipartite matching",
        "iterations_" + file_name,
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
    # print("starting experiment for Renyi-Erdos graphs")
    # average_time_experiment(
    #     Graph.generate_erdos_renyi_graph,
    #     0.1,
    #     "renyi_erdos.png",
    #     "average time to compute max flow Renyi-Erdos",
    #     [FlowAlg.EDMONDS_KARP, FlowAlg.DINITZ],
    #     "Renyi-Erdos",
    #     100,
    # )

    # print("starting experiment for Barabasi-Albert graphs")
    # average_time_experiment(
    #     Graph.generate_barabasi_albert_graph,
    #     15,
    #     "barabasi_albert.png",
    #     "average time to compute max flow Barabasi-Albert",
    #     [FlowAlg.EDMONDS_KARP, FlowAlg.DINITZ],
    #     "Barabasi-Albert",
    #     100,
    # )

    print("starting experiment for bipartite matching")
    bipartite_reduction_experiment(
        Graph.generate_erdos_renyi_bipartite_graph,
        0.1,
        "bipartite.png",
        "average time to compute max bipartite matching size",
        [FlowAlg.EDMONDS_KARP, FlowAlg.DINITZ],
        100,
    )
