# Repository containing work related to Constrained Shortest Path research, as part of the Honours Programme 

## Current roadmap:

- [x] Code basic version of shortest path between two nodes of a given graph. (no constraints)
- [x] Code version mentioned in the general workflow - mandatory vertex constraints added to the shortest path.
- [ ] Automated testing to quantify speed and efficiency of different solvers.

##Current problems:

1. Cannot make a custom-sized array to generate the actual shortest path. Currently, I am declaring a fixed-sized array that has the first x positions filled with the starting node to fill the whole array, only to afterwards fill the nodes on the path to the last node. 