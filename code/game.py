import numpy as np
import sys
import pandas as pd
import classes
import board
import breadth_first as bf
import depth_first as df
from visualization import visualize
from user_input import user_input
from algorithm_random import Random_algorithm as ra
import csv
import os
import copy
from time import time
from helpers import export_bfs_to_csv, export_results_to_csv, export_hillclimber_to_csv
from animation import animate
from hill_climb import hillclimb as hc
from run_random_algorithm import run_random

def game(filepath, rounds, algorithm, size, hill_climb = False):
    """
    Takes csv file containing vehicles and adds them to game.
    Creates dictionary containing all car instances in game.
    Generates board with cars in their starting position.
    Takes input from user and makes moves based on this input.
    """
    cars = pd.read_csv(filepath)
    iterations_list = []
    mean_i = 0
    
    min_iterations = 10000
    min_iterations_config = {}
    start = time()

    if size == 6:
        end_position = [(2,4), (2, 5)]
    elif size == 9:
        end_position = [(4, 7), (4, 8)]
    elif size == 12:
        end_position = [(5, 10), (5, 11)]

    cars_dict = {}
    # Loop over cars dataframe, create vehicles and store them in dictionary
    for idx, row in cars.iterrows():
        ID = 0
        for letter in row['car']:
            ID += ord(row['car'])
        vehicle = classes.Vehicle(ID, row['orientation'], row['col'], row['row'], row['length'])
        cars_dict[ID] = vehicle

    if algorithm == 'random':
        print(rounds)
        results = run_random(filepath, rounds, algorithm, size, end_position, hill_climb)
        return results
    elif algorithm == 'bfs':
        bf_alg = bf.breadth_first_algorithm(size)
        path = bf_alg.search_breadth(cars_dict)
        return path
    elif algorithm == 'dfs':
        df_alg = df.depth_first_algorithm(size)
        path = df_alg.search_depth(cars_dict)
        return path
    elif algorithm == 'hillclimb':
        hc_alg = hc(filepath, end_position, size)
        results = hc_alg.run_hc()
        return results
        
    # Calculate the mean iterations and return the list of iterations
    mean_i = mean_i/rounds
    # print (f'the mean amount of iterations over {rounds} rounds is {mean_i}')
    print ("iteration list:", iterations_list)

    if hill_climb:
        return min_iterations_config
    else:
        return iterations_list


if __name__ == '__main__':
    if not os.path.exists('results'):
        os.makedirs('results')
    
    # Set default values
    game_number = 0
    algorithm = ''
    rounds = 1

    if len(sys.argv) < 3:
        print("Usage: python game.py <game_number> <algorithm> [<rounds>]")
        sys.exit(1)
    
    game_number = int(sys.argv[1])
    algorithm = sys.argv[2]
    rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    if game_number in [1, 2, 3]:
        size = 6
        filepath = f'data/Rushhour6x6_{str(game_number)}.csv'
        
    elif game_number in [4, 5, 6]:
        size = 9
        filepath = f'data/Rushhour9x9_{str(game_number)}.csv'
        
    elif game_number == 12:
        size = 12
        filepath = f'data/Rushhour12x12_{str(game_number)}.csv'

    start_time = time()
    results = game(filepath, rounds, algorithm, size)
    end_time = time()
    duration = end_time - start_time
    print("Experiment results: \n", results)
    print(f"Experiment duration: {duration:.2f} seconds")
    experiment_name = f'{algorithm}_{size}x{size}_{game_number}_{rounds}'
    
    
    if algorithm == 'random':
        export_hillclimber_to_csv(f'results/{experiment_name}.csv', results)
    elif algorithm in ['bfs', 'dfs']:
        export_bfs_to_csv(f'results/{experiment_name}.csv', results)
    elif algorithm == 'hillclimb':
        export_hillclimber_to_csv(f'results/{experiment_name}.csv', results)
    
    animate(filepath, f'results/{experiment_name}.csv', size)
        # TODO: implement exporting of results

    # export_bfs_to_csv(f'results/{experiment_name}.csv', results)
    # experiment_name = 'random_2'
    # export_results_to_csv(f'results/{experiment_name}_{rounds}.csv', results)
    
    

    