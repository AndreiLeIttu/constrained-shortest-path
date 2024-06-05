use std::env;
use std::collections::VecDeque;

fn main() {
    let args: Vec<usize> = env::args()
        .skip(1)
        .map(|arg| arg.parse().expect("Argument is not of type usize"))
        .collect();

    let nodes: usize = args[0];
    let edges: usize = args[1];

    println!("{}", nodes);

    let mut index = 2;
    let mut neigh: Vec<Vec<usize>> = vec![vec![]; nodes + 1];
    let mut pre: Vec<Vec<(usize, usize, usize)>> = vec![vec![]; nodes + 2];
    let mut deg: Vec<usize> = vec![0; nodes + 2];
    
    for _ in 0..edges {
        let a: usize = args[index];
        let b: usize = args[index + 1];
        let t: usize = args[index + 2];
        let cost: usize = args[index + 3];
        index += 4;

        neigh[a].push(b);
        pre[b].push((a, t, cost));
        //not source
        if a != 0 {
            deg[b] += 1;
        }
    }

    //time windows
    let mut time_w: Vec<(usize, usize)> = vec![(0, 0); nodes + 1];
    for i in 1..=nodes {
        let start: usize = args[index];
        let end: usize = args[index + 1];
        time_w[i] = (start, end);
        index += 2;
    }

    let mut node_costs: Vec<usize> = vec![0; nodes + 2];
    for i in 1..=nodes + 1 {
        node_costs[i] = args[index];
        index += 1;
    }

    //topological sort
    let mut ordering: Vec<usize> = vec![0; nodes + 1];
    let mut cnt: usize = 0;
    let mut queue: VecDeque<usize> = VecDeque::new();
    
    for i in 1..=nodes {
        if deg[i] == 0 {
            queue.push_back(i);
        }
    }

    while let Some(x) = queue.pop_front() {
        ordering[cnt] = x;
        cnt += 1;
        for &neighbor in &neigh[x] {
            deg[neighbor] -= 1;
            if deg[neighbor] == 0 && neighbor != nodes+1 {
                queue.push_back(neighbor);
            }
        }
    }

    //dp initialization
    let mut ans: Vec<Vec<usize>> = vec![vec![1_000_000_000; 0]; nodes + 1];

    for i in 0..=nodes {
        let size = time_w[i].1 - time_w[i].0 + 1;
        ans[i] = vec![1_000_000_000; size];
    }
    ans[0][0] = 0;

    //dp
    for i in 0..nodes {
        let node = ordering[i];
        for &(prev, t, cost) in &pre[node] {
            for itr in time_w[prev].0..=time_w[prev].1 {
                if ans[prev][itr - time_w[prev].0] != 1_000_000_000 {
                    let arrival = itr + t;
                    if arrival <= time_w[node].1 {
                        let index = (arrival - time_w[node].0).max(0);
                        ans[node][index] = ans[node][index]
                            .min(ans[prev][itr - time_w[prev].0] + cost + (arrival - time_w[node].0).max(0) * node_costs[node]);
                        //println!("ans[{}][{}] = {}", node, prev, ans[node][index]);
                    }
                }
            }
        }
    }

    //sink node final node computation
    let mut res = 1_000_000_000;
    for &(prev, t, cost) in &pre[nodes + 1] {
        for itr in time_w[prev].0..=time_w[prev].1 {
            if ans[prev][itr - time_w[prev].0] != 1_000_000_000 {
                let arrival = itr + t;
                println!("arrival: {} from {}", arrival, prev);
                res = res.min(ans[prev][itr - time_w[prev].0] + cost + arrival * node_costs[nodes + 1]);
            }
        }
    }

    println!("{}", res);
}