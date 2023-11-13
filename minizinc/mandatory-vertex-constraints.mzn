int: N; %number of nodes in the graph
int: M; %number of constraints
int: start; %starting node
int: end; %ending node

array[1..N, 1..N] of int: cost; %cost matrix
array[1..M] of set of int: v_constraint; %constraint sets

set of int: interval = 1..N;

array[0..N] of var int: road; 

%constraints

constraint road[0]=start;
constraint road[N]=end;

constraint forall(constr in v_constraint) (
    exists(i in constr) (i in array2set(road))
);

constraint forall(i in interval) (
  cost[road[i-1], road[i]]!=-1);

solve minimize sum(i in 1..N)(cost[road[i-1],road[i]])