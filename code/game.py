import numpy as np
import pandas as pd
import classes
import board
import breadth_first as bf
from visualization import visualize
from user_input import user_input
from algorithm_random import Random_algorithm as ra
import csv
import os
import copy
from time import time
from helpers import export_bfs_to_csv, export_results_to_csv


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
    round = 1
    min_iterations = float('inf')
    min_iterations_config = {}
    start = time()
<<<<<<< HEAD
    
=======

    step_counter = 0
    print(f"Initial step_counter: {step_counter}")

    if size == 6:
            end_position = [(2,4), (2, 5)]
    elif size == 9:
        end_position = [(4, 7), (4, 8)]
    elif size == 12:
        end_position = [(5, 10), (5, 11)]

>>>>>>> 7e82c5cf2cfdd19f07796a9c5f8eca8f2db2fb50
    for _ in range (rounds):
        
        cars_dict = {}
        # Loop over cars dataframe, create vehicles and store them in dictionary
        for idx, row in cars.iterrows():
            ID = 0
            for letter in row['car']:
                ID += ord(row['car'])
            vehicle = classes.Vehicle(ID, row['orientation'], row['col'], row['row'], row['length'])
            cars_dict[ID] = vehicle

        # Initialise board and add cars in starting positions
        game_board = board.Board(cars_dict, size)

        if algorithm == 'random':
            # Initiate random step
            random_exp = ra(cars_dict, game_board)

            # track current config
            current_config = {}
            i = 0
<<<<<<< HEAD
            step_counter = 0

            # while the red car is not yet in the right position, the algorithm goes on
            while cars_dict[ord('X')].position != [(2,4), (2,5)]:
=======
            while cars_dict[ord('X')].position != end_position:
>>>>>>> 7e82c5cf2cfdd19f07796a9c5f8eca8f2db2fb50
                random_exp.random_step(hill_climb)
                if hill_climb:
                    current_config[step_counter] = random_exp.copy_cars_dict()
                i +=1
                step_counter += 1
                if i > min_iterations:
                    break
            print(f"Round {round}, Iterations: {i}, Min Iterations: {min_iterations}")


                


            # Save the amount of iterations and use it to calculate the mean
            iterations_list.append(i)
            mean_i += i
            if round % 100 == 0:
                end = time()
                print(f'The time elapsed: {end-start:.2f} seconds.')
                print(f"progress:{(round/rounds) * 100}")
                start = time()
            round += 1

            if hill_climb and i < min_iterations:
                min_iterations = i
                min_iterations_config = current_config

        elif algorithm == 'bfs':
            bf_alg = bf.breadth_first_algorithm(size)
            path = bf_alg.search_breadth(cars_dict)
            return path

        
        

    # Calculate the mean iterations and return the list of iterations
    mean_i = mean_i/rounds
    # print (f'the mean amount of iterations over {rounds} rounds is {mean_i}')
    print ("iteration list:", iterations_list)

    if hill_climb:
        return iterations_list, min_iterations_config
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
        
    while algorithm not in ['random', 'bfs', 'hillclimb']:
        algorithm = input("Which algorithm would you like to use? Enter one of the following: \n- random \n- bfs \n- hillclimb \nAlgorithm: ")
    
    if algorithm in ['random', 'hillclimb']:
        rounds = int(input("How many rounds would you like the algorithm to search? "))
        

    if game_number in [1, 2, 3]:
        filepath = f'data/Rushhour6x6_{str(game_number)}.csv'
        results = game(filepath, rounds, algorithm, size=6)
        experiment_name = f'{algorithm}_6x6_{game_number}_{rounds}'

    elif game_number in [4, 5, 6]:
        filepath = f'data/Rushhour9x9_{str(game_number)}.csv'
        results = game(filepath, rounds, algorithm, size=9)
        experiment_name = f'{algorithm}_9x9_{game_number}_{rounds}'
    
    elif game_number == 12:
        filepath = f'data/Rushhour12x12_{str(game_number)}.csv'
        results = game(filepath, rounds, algorithm, size=12)
        experiment_name = f'{algorithm}_12x12_{game_number}_{rounds}'

    if algorithm == 'random':
        export_results_to_csv(f'results/{experiment_name}.csv', results)
    elif algorithm == 'bfs':
        export_bfs_to_csv(f'results/{experiment_name}.csv', results)
    # elif algorithm == 'hillclimb':
        # TODO: implement exporting of results

    # export_bfs_to_csv(f'results/{experiment_name}.csv', results)
    # experiment_name = 'random_2'
    # export_results_to_csv(f'results/{experiment_name}_{rounds}.csv', results)
    
    
    
    #TODO: fix bfs for board 1.
    