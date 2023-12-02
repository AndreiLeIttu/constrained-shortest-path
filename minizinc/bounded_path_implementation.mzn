
include "globals.mzn";
int: N;
int: E;
int: C;

var 1..N: source;
var 1..N: target;

array[1..E] of int: from;
array[1..E] of int: to;
array[1..E] of int: weights;
array[1..C] of set of int: v_constraint; 

array[1..N] of var bool: nodes_on_path;
array[1..E] of var bool: edges_on_path;

var int: path_cost;

constraint bounded_path(from, to, weights, source, target, nodes_on_path, edges_on_path, path_cost);

constraint forall(constr in v_constraint) (
    exists(i in constr)(nodes_on_path[i])
);

solve minimize path_cost;