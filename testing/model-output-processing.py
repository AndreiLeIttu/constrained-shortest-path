#look at the ./outputs/dp-experiments/1 folder, and inside, for each subfolder from 0 to 49, print the metrics and stdout files
import os
import json
import re
from pathlib import Path
from collections import defaultdict

def extract_total_time_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()
            if line == "[wall_micros]":
                if i + 2 < len(lines):
                    total_time = int(lines[i+1].split('=')[1].strip()) + int(lines[i+2].split('=')[1].strip()) / 1_000_000_000
                    i+=2
                    break
            i+=1

    return total_time

def process_experiment_folder(folder_path, flag):
    metrics_file = folder_path / 'metrics'
    stdout_file = folder_path / 'stdout'

    if stdout_file.exists():
        with open(stdout_file, 'r') as f:
            lines = f.readlines()
            if flag == "dp" and lines[1].startswith("No valid path"):
                return -1
            elif flag == "cp" and "UNSATISFIABLE" in lines[0]:
                return -1

    if metrics_file.exists():
        time = extract_total_time_from_file(metrics_file)
        return time

def main():

    base_dp_path = Path('./outputs/dp-experiments/1/0')
    time_windows_propagator_path = Path('./outputs/mzn-experiments/1/1')
    baseline_cp_path = Path('./outputs/mzn-experiments/1/0')

    times = []


    for experiment_folder in base_dp_path.iterdir():
        if experiment_folder.is_dir():
            time = process_experiment_folder(experiment_folder, "dp")
            times.append(time)

    average_time = sum(t for t in times if t != -1) / len([t for t in times if t != -1])
    print(f"Average dp time: {average_time:.2f} seconds")

    times = []

    for experiment_folder in time_windows_propagator_path.iterdir():
        if experiment_folder.is_dir():
            time = process_experiment_folder(experiment_folder, "cp")
            times.append(time)

    average_time = sum(t for t in times if t != -1) / len([t for t in times if t != -1])
    print(f"Average time windows propagator time: {average_time:.2f} seconds")

    times = []

    for experiment_folder in baseline_cp_path.iterdir():
        if experiment_folder.is_dir():
            time = process_experiment_folder(experiment_folder, "cp")
            times.append(time)

    average_time = sum(t for t in times if t != -1) / len([t for t in times if t != -1])
    print(f"Average baseline cp time: {average_time:.2f} seconds")

if __name__ == "__main__":
    main()