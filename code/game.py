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


def game(filepath, rounds, algorithm, hill_climb = False):
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
        game_board = board.Board(cars_dict, size=6)

        if algorithm == 'random':
            # Initiate random step
            random_exp = ra(cars_dict, game_board)

            # track current config
            current_config = {}
            i = 0
            step_counter = 0

            # while the red car is not yet in the right position, the algorithm goes on
            while cars_dict[ord('X')].position != [(2,4), (2,5)]:
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

        elif algorithm == 'bf':
            bf_alg = bf.breadth_first_algorithm(6)
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
    
    rounds = 1
    algorithm = 'bf'

    filepath = 'data/Rushhour6x6_2.csv'
    results = game(filepath, rounds, algorithm)
    print(results)

    experiment_name = 'bfs_6x6_2'
    export_bfs_to_csv(f'results/{experiment_name}.csv', results)
    # experiment_name = 'random_2'
    # export_results_to_csv(f'results/{experiment_name}_{rounds}.csv', results)
    
    