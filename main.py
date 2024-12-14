import time

from flow import FlowNetwork
from graph import Graph

if __name__ == "__main__":
    graph: Graph = Graph()

    total_time = 0
    for i in range(100):
        flow = FlowNetwork(70, Graph.generate_erdos_renyi_graph(70, 0.1, 70), 0, 69)
        start_time = time.time()
        val_f = sum(flow.compute_max_flow()[0])
        end_time = time.time()
        total_time += end_time - start_time

        print("max flow is", val_f, "and took time to run:", end_time - start_time)

    print("average time is ", total_time / 100)
