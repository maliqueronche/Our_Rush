import numpy as np
import pandas as pd
import classes
import board
import breadth_first as bf
import depth_first as df
from algorithm_random import Random_algorithm as ra
import iterative_deepening as it
from time import time, sleep, strftime, gmtime
from helpers import export_bfs_to_csv, export_results_to_csv
import os

def game(filepath, algorithm, size, heuristic=False, max_time=None):
    """
    Runs the specified algorithm on the given board configuration.

    Args:
        filepath (str): Path to the CSV file containing car information.
        algorithm (str): The algorithm to use ('bfs', 'dfs', 'itdp', 'random').
        size (int): The size of the board (6, 9, or 12).
        heuristic (bool): Whether to use the heuristic for the DFS algorithm.
        max_time (int): Maximum time allowed for the algorithm in seconds.

    Returns:
        results (list or path): The result of the algorithm, either the solution path or list of iterations.
    """
    cars = pd.read_csv(filepath)

    # Set end position based on board size
    if size == 6:
        end_position = [(2, 4), (2, 5)]
    elif size == 9:
        end_position = [(4, 7), (4, 8)]
    elif size == 12:
        end_position = [(5, 10), (5, 11)]

    cars_dict = {}
    
    # Create vehicles and store them in dictionary
    for idx, row in cars.iterrows():
        ID = sum(ord(letter) for letter in row['car'])
        vehicle = classes.Vehicle(ID, row['orientation'], row['col'], row['row'], row['length'])
        cars_dict[ID] = vehicle

    start_time = time()
    if algorithm == 'bfs':
        bf_alg = bf.breadth_first_algorithm(size)
        path = bf_alg.search_breadth(cars_dict)
        return path

    elif algorithm == 'dfs':
        df_alg = df.depth_first_algorithm(size)
        path = df_alg.search_depth(cars_dict, bb=heuristic)
        return path

    elif algorithm == 'itdp':
        itdp_alg = it.iterative_deepening_algorithm(size)
        results = itdp_alg.search_depth_iteratively(cars_dict)
        return results

    elif algorithm == 'random':
        best_result = None
        best_results = None
        while time() - start_time < max_time:
            results = ra(filepath, 1, algorithm, size, end_position)
            iterations = len(results)
            if best_result is None or iterations < best_result:
                best_result = iterations
                best_results = results
            # Check every five minutes
            if (time() - start_time) % 300 < 1:
                elapsed_time = time() - start_time
                remaining_time = max_time - elapsed_time
                print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Remaining time for {algorithm} on board {size}: {remaining_time / 60:.2f} minutes")
        return best_results

def run_experiments():
    """
    Runs all the specified experiments back-to-back.
    """
    experiments = [
        # BFS for boards 1, 2, and 3
        {"algorithm": "bfs", "boards": [1, 2, 3], "size": 6, "max_time": None},
        # BFS for boards 4, 5, and 6 with 1-hour time limit
        {"algorithm": "bfs", "boards": [4, 5, 6], "size": 9, "max_time": 3600},
        # ITDP for every experiment with 30-minute time limit
        {"algorithm": "itdp", "boards": [1, 2, 3, 4, 5, 6], "size": [6, 9], "max_time": 1800},
        # DFS for every experiment with 30-minute time limit
        {"algorithm": "dfs", "boards": [1, 2, 3, 4, 5, 6], "size": [6, 9], "max_time": 1800},
        # Random for every experiment with 30-minute time limit
        {"algorithm": "random", "boards": [1, 2, 3, 4, 5, 6], "size": [6, 9], "max_time": 1800},
        # Random for board 7 with 30-minute time limit
        {"algorithm": "random", "boards": [7], "size": 12, "max_time": 1800},
    ]

    for exp in experiments:
        for board in exp["boards"]:
            size = exp["size"]
            if isinstance(size, list):
                size = size[0] if board <= 3 else size[1]
            filepath = f'data/Rushhour{size}x{size}_{board}.csv'
            algorithm = exp["algorithm"]
            max_time = exp["max_time"]

            print(f"Running {algorithm} for board {board} with size {size}x{size}")

            start_time = time()
            result = game(filepath, algorithm, size, heuristic=(algorithm == 'dfs'), max_time=max_time)
            duration = time() - start_time
            print(f"Experiment duration: {duration:.2f} seconds")

            if result:
                experiment_name = f'{algorithm}_{size}x{size}_{board}'
                export_bfs_to_csv(f'results/{experiment_name}.csv', result)
                print(f"Results exported to results/{experiment_name}.csv")

            # Check every five minutes how much time is remaining
            while True:
                if (time() - start_time) % 300 < 1:
                    elapsed_time = time() - start_time
                    remaining_time = max_time - elapsed_time
                    print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Remaining time for {algorithm} on board {board}: {remaining_time / 60:.2f} minutes")
                if max_time and duration >= max_time:
                    print(f"Experiment {algorithm} for board {board} timed out.")
                    break

if __name__ == '__main__':
    # Ensure the results directory exists
    if not os.path.exists('results'):
        os.makedirs('results')
    
    run_experiments()