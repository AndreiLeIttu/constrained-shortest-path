int: N;
int: M;
int: start;
int: end;

array[1..N, 1..N] of int: cost;
array[1..M] of set of int: v_constraint;

set of int: interval = 1..N;

array[0..N] of var int: road;

constraint road[0]=start;
constraint road[N]=end;

constraint forall(constr in v_constraint) (
    exists(i in constr) (i in array2set(road))
);

constraint forall(i in interval) (
  cost[road[i-1], road[i]]!=-1);

solve minimize sum(i in 1..N)(cost[road[i-1],road[i]])