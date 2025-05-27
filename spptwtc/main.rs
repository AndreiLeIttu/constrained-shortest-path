use std::env;
use std::fs;
use std::collections::VecDeque;

fn main() {
    let pre_args: Vec<String> = env::args().collect();
    let file_path = &pre_args[1];
    let input = fs::read_to_string(file_path).expect("Failed to read input file");
    let args: Vec<usize> = input.split_whitespace()
        .map(|s| s.parse().expect("Failed to parse number"))
        .collect();

    let nodes: usize = args[0];
    let edges: usize = args[1];

    let mut index = 2;
    let mut neigh: Vec<Vec<(usize, usize)>> = vec![vec![]; nodes + 1];
    let mut pre: Vec<Vec<(usize, usize, usize)>> = vec![vec![]; nodes + 2];
    let mut deg: Vec<usize> = vec![0; nodes + 2];
    
    for _ in 0..edges {
        let a: usize = args[index];
        let b: usize = args[index + 1];
        let t: usize = args[index + 2];
        let cost: usize = args[index + 3];
        index += 4;

        neigh[a].push((b,t));
        pre[b].push((a, t, cost));
        //not source
        if a != 0 {
            deg[b] += 1;
        }
    }

    //time windows
    let mut time_w: Vec<(usize, usize)> = vec![(0, 0); nodes + 2];
    for i in 1..=nodes+1 {
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
        for &(neighbor, _) in &neigh[x] {
            deg[neighbor] -= 1;
            if deg[neighbor] == 0 && neighbor != nodes+1 {
                queue.push_back(neighbor);
            }
        }
    }

    // //constraining the start of the time windows
    // for i in 0..nodes {
    //     let node = ordering[i];
    //     let mut min_start = 1_000_000_000;
    //     for &(prev, t, _) in &pre[node] {
    //         min_start = min_start.min(time_w[prev].0 + t);
    //     }
    //     time_w[node].0 = time_w[node].0.max(min_start)
    // }

    // //constraining the end of the time windows
    // for i in (0..nodes).rev() {
    //     let node = ordering[i];
    //     let mut max_end = 0;
    //     for &(next, t) in &neigh[node] {
    //         if next != nodes+1 {
    //             max_end = max_end.max(time_w[next].1-t);
    //         }
    //     }
    //     if max_end != 0 {
    //         time_w[node].1 = time_w[node].1.min(max_end);
    //     }
    // }

    // println!("{:?}", time_w);

    //dp initialization
    let mut ans: Vec<Vec<usize>> = vec![vec![1_000_000_000; 0]; nodes + 1];
    let mut res = 1_000_000_000;

    for i in 0..=nodes {
        let size = time_w[i].1 - time_w[i].0 + 1;
        ans[i] = vec![1_000_000_000; size];
    }
    ans[0][0] = 0;

    let mut parent: Vec<Vec<Option<(usize, usize)>>> = vec![vec![None; 0]; nodes + 2];
    for i in 0..=nodes+1 {
        let size = time_w[i].1 - time_w[i].0 + 1;
        parent[i] = vec![None; size];
    }

    let mut final_arrival_time = 1_000_000_000;

    //dp
    for i in 0..=nodes {
        let node = if i < nodes { ordering[i] } else { nodes + 1 };

        for &(prev, t, cost) in &pre[node] {
            for itr in time_w[prev].0..=time_w[prev].1 {
                let prev_index = itr - time_w[prev].0;
                if ans[prev][prev_index] != 1_000_000_000 {
                    let arrival = itr + t;
                    if arrival > time_w[node].1 {
                        continue;
                    }

                    let index = (arrival as isize - time_w[node].0 as isize).max(0) as usize;
                    let cost_here = ans[prev][prev_index] + cost + index * node_costs[node];

                    if node != nodes + 1 {
                        if cost_here < ans[node][index] {
                            ans[node][index] = cost_here;
                            parent[node][index] = Some((prev, prev_index));
                        }
                    } else {
                        if cost_here < res {
                            res = cost_here;
                            parent[node][index] = Some((prev, prev_index));
                            final_arrival_time = index;
                        }
                    }
                }
            }
        }
    }

    println!("{}", res);
    // Reconstruct best path
    let mut path = vec![];
    let mut current_node = nodes+1;
    let mut best_time_index = final_arrival_time;
    if res == 1_000_000_000 {
        println!("No valid path found.");
        return;
    }

    while current_node != 0 {
        path.push(current_node);
        if let Some((prev, new_index)) = parent[current_node][best_time_index] {
            best_time_index = new_index;
            current_node = prev;
        } else {
            break;
        }

    }

    path.push(0);
    path.reverse();

    println!("Best path: {:?}", path);

}