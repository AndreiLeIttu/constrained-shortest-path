int: N; %number of non-source or sink nodes in the graph
int: M; %number of edges in the graph

array[1..M] of tuple(int, int, int, int): edges;
array[1..N+1] of tuple(int, int): time_windows;
array[1..N+1] of int: node_costs;

%decision variables
array[1..M] of var bool: edge_on_path;
array[0..N+1] of var bool: node_on_path;
array[0..N+1] of var 0..100000: time_of_arrival;

%constraints
constraint node_on_path[0] = 1;
constraint node_on_path[N+1] = 1;
constraint time_of_arrival[0] = 0;

%ensure time window constraints are satisfied
constraint forall(i in 1..N) (
  node_on_path[i] = 1 -> (time_of_arrival[i] >= time_windows[i+1].1 /\ time_of_arrival[i] <= time_windows[i+1].2)
);

constraint forall(i in 1..M) (
  edge_on_path[i] = 1 -> time_of_arrival[edges[i].2] >= time_of_arrival[edges[i].1] + edges[i].3
);

constraint forall(i in 1..N+1) (
  node_on_path[i] = 1 -> exists(j in 1..M)(edges[j].2 = i /\ edge_on_path[j] = 1) 
);

constraint forall(i in 1..M) (
  edge_on_path[i] = 1 -> (node_on_path[edges[i].1] = 1 /\ node_on_path[edges[i].2] = 1)
);

%objective of minimizing the cost of the path
var int: total_cost = sum([edge_on_path[i] * edges[i].4 | i in 1..M]) + 
                      sum([node_on_path[i] * (time_of_arrival[i] - time_windows[i+1].1) * node_costs[i] | i in 1..N]) +
                      time_of_arrival[N+1] * node_costs[N+1]; 

solve minimize total_cost;

output [
  "Total cost: \(total_cost)",
  "\nEdge on path: ", show(edge_on_path),
  "\nNode on path: ", show(node_on_path),
  "\nTime of arrival: ", show(time_of_arrival)
];