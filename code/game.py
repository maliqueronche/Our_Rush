import numpy as np
import argparse
import pandas as pd
import classes
import board
import breadth_first as bf
import depth_first as df
from visualization import visualize
from algorithm_random import Random_algorithm as ra
import csv
import os
import copy
from time import time
from helpers import export_bfs_to_csv, export_results_to_csv, export_hillclimber_to_csv
from animation import animate
from hill_climb import hill_climber as hc
from run_random_algorithm import run_random
import iterative_deepening as it

def game(filepath, rounds, algorithm, size, heuristic):
    """
    Takes csv file containing vehicles and adds them to game.
    Creates dictionary containing all car instances in game.
    Generates board with cars in their starting position.
    Takes input from user and makes moves based on this input.
    """
    
    cars = pd.read_csv(filepath)
    iterations_list = []

    # set end position based on board size
    if size == 6:
        end_position = [(2,4), (2, 5)]
    elif size == 9:
        end_position = [(4, 7), (4, 8)]
    elif size == 12:
        end_position = [(5, 10), (5, 11)]

    if heuristic == 'bb':
        bb_ = True
    else:
        bb_ = False

    cars_dict = {}
    
    # Loop over cars dataframe, create vehicles and store them in dictionary
    for idx, row in cars.iterrows():
        ID = 0
        for letter in row['car']:
            ID += ord(letter)
        vehicle = classes.Vehicle(ID, row['orientation'], row['col'], row['row'], row['length'])
        cars_dict[ID] = vehicle

    if algorithm == 'random':
        results = run_random(filepath, rounds, algorithm, size, end_position, hill_climb = False)
        return results
    elif algorithm == 'bfs':
        bf_alg = bf.breadth_first_algorithm(size)
        path = bf_alg.search_breadth(cars_dict)
        return path
    elif algorithm == 'dfs':
        df_alg = df.depth_first_algorithm(size)
        path = df_alg.search_depth(cars_dict, bb = bb_)
        return path
    elif algorithm == 'itdp':
        itdp_alg = it.iterative_deepening_algorithm(size)
        results = itdp_alg.search_depth_iteratively(cars_dict)
        return results
    

if __name__ == '__main__':

    # esnsure the results directory exists
    if not os.path.exists('results'):
        os.makedirs('results')
    
    # argument parser for command-line arguments
    parser = argparse.ArgumentParser(description="Speel een spel met een bepaald algoritme en optionele parameters.")
    parser.add_argument('-g', '--game', required = True, type = int, help='The game number')
    parser.add_argument('-a', '--algorithm', required = True, type = str, help='The algorithm')
    parser.add_argument('-r', '--rounds', type = int, default = 1, help='Amound of rounds (default = 1)')
    parser.add_argument('-e', '--heuristic', type = str, default = False, help='Heuristic (default = 1)')
    parser.add_argument('-v', '--visualize', type = bool, default = False, help='Animation')

    args = parser.parse_args()

    game_number = args.game
    algorithm = args.algorithm
    rounds = args.rounds
    heuristic = args.heuristic
    visualization = args.visualize

    # set file path based on game number
    if game_number in [1, 2, 3]:
        size = 6
        filepath = f'data/Rushhour6x6_{str(game_number)}.csv'
    elif game_number in [4, 5, 6]:
        size = 9
        filepath = f'data/Rushhour9x9_{str(game_number)}.csv'
    elif game_number == 7:
        size = 12
        filepath = f'data/Rushhour12x12_{str(game_number)}.csv'

    # run the game and measure the duration
    start_time = time()
    results = game(filepath, rounds, algorithm, size, heuristic)
    end_time = time()
    duration = end_time - start_time
    print(f"Experiment duration: {duration:.2f} seconds")
    experiment_name = f'{algorithm}_{size}x{size}_{game_number}_{rounds}'
    
    # export results based on algorithm
    if algorithm == 'random':
        export_hillclimber_to_csv(f'results/{experiment_name}.csv', results)
    elif algorithm in ['bfs', 'dfs', 'itdp']:
        export_bfs_to_csv(f'results/{experiment_name}.csv', results)
    elif algorithm == 'hillclimb':
        export_hillclimber_to_csv(f'results/{experiment_name}.csv', results)
    
    # optionally create an animation
    if algorithm != 'random' and visualization == True:
        animate(filepath, f'results/{experiment_name}.csv', size)
       

    