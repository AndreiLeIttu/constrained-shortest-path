import networkx as nx
import random

#generate a random DAG with weights for cost and time on edges, time windows and costs for nodes
def generate_random_dag(num_nodes, edge_probability):
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                cost = random.randint(1, 10)  
                time = random.randint(1, 10)
                G.add_edge(i, j, cost=cost, time=time)
    
    for node in G.nodes():
        start = random.randint(0, 50)
        end = start + random.randint(5, 50)
        cost = random.randint(1, 10)
        G.nodes[node]['time_window']=(start, end) if node != 0 else (0, 0)
        G.nodes[node]['cost'] = cost if node != 0 else 0
    return G

for i in range(10):
    # generate 100 experiments and write them to a file
    dag = generate_random_dag(20, 0.5)
    with open(f"./testing/spptwtc/sparse_graph{i}.dzn", "w") as f:
        #number of nodes = N - 2, since the model expects the amount of non-terminal nodes
        nodesStr = "N={};\n".format(dag.number_of_nodes()-2)
        numEdgesStr = "M=" + str(dag.number_of_edges()) + ";\n"
        edgesStr = "edges=[\n"
        for u, v, data in dag.edges(data=True):
            edgesStr += f"({u},{v},{data['time']},{data['cost']}),\n"
        edgesStr += "];\n"
        windowsStr = "windows=[\n"
        for node in dag.nodes():
            if node == 0:
                continue
            time_window = dag.nodes[node]['time_window']
            windowsStr += f"({time_window[0]}, {time_window[1]}),\n"
        windowsStr += "];\n"
        costsStr = "node_costs=["
        for node in dag.nodes():
            if node == 0:
                continue
            costsStr += f"{dag.nodes[node]['cost']},"
        costsStr += "];"
        f.write(nodesStr + numEdgesStr + edgesStr + windowsStr + costsStr)