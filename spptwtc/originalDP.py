from collections import defaultdict

class Label:
    def __init__(self, time, cost, slope):
        self.time = time
        self.cost = cost
        self.slope = slope

    def __lt__(self, other):
        return (self.time, self.cost) < (other.time, other.cost)

def spptwtc_dp(nodes, edges, time_windows, durations, arc_costs, node_costs, source, sink):
    #it is assumed that the nodes are topologically sorted
    labels = defaultdict(list)
    labels[source].append(Label(time_windows[source][0], node_costs[source] * time_windows[source][0], 0))

    for j in range(nodes):
        new_labels = []
        for index, dur in enumerate(durations):
            i = edges[index][0]
            jj = edges[index][1]
            if jj != j: continue
            for label in labels[i]:
                t_j = max(time_windows[j][0], label.time + dur)
                if t_j > time_windows[j][1]: continue
                cost_j = label.cost + node_costs[j] * (t_j-time_windows[j][0]) + arc_costs[index]
                slope_j = min(0, label.slope + node_costs[j])
                new_labels.append(Label(t_j, cost_j, slope_j))
        new_labels.sort()
        pruned = []
        for l in new_labels:
            if not pruned or l.cost < pruned[-1].cost:
                pruned.append(l)
        labels[j].extend(pruned)
        print(min(label.cost for label in labels[j]), j)

    return min(label.cost for label in labels[sink])

#read input from file
with open('./input.in', 'r') as f:
    lines = f.readlines()
    line0 = lines[0].strip().split(' ')
    nodes = int(line0[0]) + 2  # +2 for source and sink
    num_edges = int(line0[1])
    edge_costs = []
    edge_times = []
    edges = []
    for i in range(1, num_edges + 1):
        line = lines[i].strip().split(' ')
        u = int(line[0])
        v = int(line[1])
        edge_times.append(int(line[2]))
        edge_costs.append(int(line[3]))
        edges.append((u, v))
    time_windows = []
    time_windows.append((0, 0))  # time window for source node
    node_costs = []
    node_costs.append(0)  # cost for source node
    for i in range(num_edges + 1, num_edges + nodes):
        line = lines[i].strip().split(' ')
        time_windows.append((int(line[0]), int(line[1])))
    line = lines[num_edges + nodes].strip().split(' ')
    for i in range(len(line)):
        node_costs.append(int(line[i]))

    print(spptwtc_dp(nodes, edges, time_windows, edge_times, edge_costs, node_costs, 0, nodes - 1))