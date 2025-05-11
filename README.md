# Repository containing work related to Constrained Shortest Path research, as part of the Honours Programme 

## Current roadmap:

- Started with the mandatory vertices constraint, but found out that a lot of work is already done in this area
- Changed directions to time window constraints, based on the paper [link paper]
- Implemented DP algorithm based on the assumption of only non-negative node costs.
- Implemented basic CP model of the shortest path problem with time window and node costs
- Implemented a new global constraint called `time_windows`, and a new propagator corresponding to it
- Currently comparing existing solution vs DP vs basic CP model vs model with the `time_windows` propagator