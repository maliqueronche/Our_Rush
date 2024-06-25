import numpy as np
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

from hill_climb import hill_climber as hc
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

    # step_counter = 0
    # print(f"Initial step_counter: {step_counter}")

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

    #     # Initialise board and add cars in starting positions
    #     game_board = board.Board(cars_dict, size)

    #     if algorithm in ['random']:

            

    #     #     # Initiate random step
    #     #     random_exp = ra(cars_dict, game_board)

    #     #     # track current config
    #     #     current_config = {}
    #     #     i = 0

    #     #     while cars_dict[ord('X')].position != end_position:

    #     #         # for hill climb, save new board, every step
    #     #         if hill_climb:
    #     #             random_exp.random_step(hill_climb = True)
    #     #             cars_dict = random_exp.cars
    #     #             current_config[i] = random_exp.copy_cars_dict(cars_dict)

    #     #             if i > min_iterations:
    #     #                 break

    #     #         else:
    #     #             random_exp.random_step()
                
    #     #         i +=1
                
                
    #     #     # print(f"Round {round}, Iterations: {i}, Min Iterations: {min_iterations}")

    #     #     # Save the amount of iterations and use it to calculate the mean
    #     #     iterations_list.append(i)
    #     #     mean_i += i
    #     #     if round % 100 == 0:
    #     #         end = time()
    #     #         print(f'The time elapsed: {end-start:.2f} seconds.')
    #     #         print(f"progress:{(round/rounds) * 100}")
    #     #         start = time()
    #     #     round += 1

    #     #     if hill_climb and i < min_iterations:
    #     #         min_iterations = i
    #     #         min_iterations_config = random_exp.copy_cars_dict(current_config)

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

    # Keep looping over user prompts while answers are wrong
    while game_number < 1 or game_number > 7:
        game_number = int(input("Hi, which game of Rush Hour (1-7) would you like to play? "))
        
    while algorithm not in ['random', 'bfs', 'dfs', 'hillclimb']:
        algorithm = input("Which algorithm would you like to use? Enter one of the following: \n- random \n- bfs \n- dfs \n- hillclimb \nAlgorithm: ")
    
    if algorithm in ['random']:
        rounds = int(input("How many rounds would you like the algorithm to search? "))
        

    if game_number in [1, 2, 3]:
        size = 6
        filepath = f'data/Rushhour6x6_{str(game_number)}.csv'
        results = game(filepath, rounds, algorithm, size)
        print(results)
        experiment_name = f'{algorithm}_6x6_{game_number}_{rounds}'
        animate(filepath, f'results/{experiment_name}.csv', size)

    elif game_number in [4, 5, 6]:
        size = 9
        filepath = f'data/Rushhour9x9_{str(game_number)}.csv'
        results = game(filepath, rounds, algorithm, size)
        experiment_name = f'{algorithm}_9x9_{game_number}_{rounds}'
        animate(filepath, f'results/{experiment_name}.csv', size)
    
    elif game_number == 12:
        size = 12
        filepath = f'data/Rushhour12x12_{str(game_number)}.csv'
        results = game(filepath, rounds, algorithm, size)
        experiment_name = f'{algorithm}_12x12_{game_number}_{rounds}'
        animate(filepath, f'results/{experiment_name}.csv', size)

    
    if algorithm == 'random':
        export_hillclimber_to_csv(f'results/{experiment_name}.csv', results)
    elif algorithm in ['bfs', 'dfs']:
        export_bfs_to_csv(f'results/{experiment_name}.csv', results)
    elif algorithm == 'hillclimb':
        export_hillclimber_to_csv(f'results/{experiment_name}.csv', results)
        # TODO: implement exporting of results

    
    
    
    # export_bfs_to_csv(f'results/{experiment_name}.csv', results)
    # experiment_name = 'random_2'
    # export_results_to_csv(f'results/{experiment_name}_{rounds}.csv', results)
    
    

    