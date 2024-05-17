#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_set>

using namespace std;

ifstream in("input.in");
ofstream out("output.out");

int main() {
    int nodes,edges;
    in>>nodes>>edges;
    vector<int> ordering(nodes+1);
    vector<int> node_costs(nodes+2);
    vector<pair<int,int>> time_w(nodes+1);
    vector<tuple<int,int,int>> pre[nodes+2];
    vector<int> neigh[nodes+1];
    int deg[nodes+1]={0};
    for (int i=1;i<=edges;i++) {
        int a,b,t,cost;
        in>>a>>b>>t>>cost;
        neigh[a].push_back(b);
        pre[b].push_back(make_tuple(a,t,cost));
        if (a) //not source 
            deg[b]++;
    }
    //time windows
    for (int i=1;i<=nodes;i++)
        in>>time_w[i].first>>time_w[i].second;
    vector<int>ans[nodes+1];
    ans[0].push_back(0);
    for (int i=1;i<=nodes;i++) {
        for (int j=0;j<=time_w[i].second-time_w[i].first;j++)
            ans[i].push_back(1e9);
    }
    time_w[0].first=time_w[0].second=0;
    //node costs
    for (int i=1;i<=nodes+1;i++)
        in>>node_costs[i];
    //maybe a bfs/dfs before to mark nodes that cannot be reached from the source
    
    //topological sort
    int cnt=0;
    for (int i=1;i<=nodes;i++) {
        if (deg[i]==0)
            ordering[++cnt]=i;
    }
    for (int i=1;i<=nodes;i++) {
        int x = ordering[i];
        for (int j=0;j<neigh[x].size();j++) {
            deg[neigh[x][j]]--;
            if (!deg[neigh[x][j]])
                ordering[++cnt]=neigh[x][j];
        }
    }
    //dp
    for (int i=1;i<=nodes;i++) {
        int node = ordering[i];
        for (const auto& [prev, t, cost]: pre[node]) {
            for (int itr = time_w[prev].first;itr<=time_w[prev].second;itr++) {
                if (ans[prev][itr-time_w[prev].first]!=1e9) {
                    int arrival = itr + t;
                    if (arrival<=time_w[node].second) {
                        ans[node][max(arrival-time_w[node].first, 0)] = min(ans[node][max(arrival-time_w[node].first, 0)], ans[prev][itr-time_w[prev].first]+cost+max(0, arrival-time_w[node].first)*node_costs[node]);
                        out<<ans[node][max(arrival-time_w[node].first, 0)]<<" "<<node<<" "<<prev<<'\n';
                    }
                }
            }
        }
    }
    //sink node final cost computation
    int res = 1e9;
    for (const auto& [prev, t, cost]: pre[nodes+1]) {
        for (int itr = time_w[prev].first;itr<=time_w[prev].second;itr++) {
                if (ans[prev][itr-time_w[prev].first]!=1e9) {
                    int arrival = itr + t;
                    out<<arrival<<" "<<prev<<" "<<'\n';
                    res = min(res, ans[prev][itr-time_w[prev].first]+cost+arrival*node_costs[nodes+1]);
                }
            }
    }
    out<<res;
    return 0;
}

/*
Assuming non-negative node costs, each node needs to be visited as soon as possible. There is 
still a choice to be made about the best time between [a_i, b_i] to visit node i (depending on the path we take up until the current node),
but we have no reason to ever wait before starting the service at node i(except if we get there before its time window starts), 
since the non-negative cost implies that each node should be visited as early as possible when given this choice.

Steps: 
1. Topological sorting of the graph
2. For each node (in the topological order)
    2.1 For each predecessor of the node
        2.2 For each possibility of the service starting times for the predecessor (b_predecessor-a_predecessor+1 options)
            ans(current node, time_at_predecessor+edge duration) = min(ans(predecessor, time_at_predecessor) + edge cost + waiting_time * node cost)

Time complexity O(n^2*max(b-a)) - for each node, go through each of its predecessors, and go through each of the predecessor's possible
service starting times(time window of the predecessor).
*/

/*
4 6 
0 1 2 1
0 2 4 1
2 4 2 1 
1 3 2 1 
3 4 2 1 
4 5 3 3
1 100
1 100 
1 100 
1 100
1 5 1 1 1
*/
/*
2 4
0 1 3 3 
1 3 0 0 
2 3 0 0 
0 2 1 1 
1 100 
1 100
1 1 1
*/