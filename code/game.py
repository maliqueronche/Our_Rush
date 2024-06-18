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
        game_board = board.Board(cars_dict)

        if algorithm == 'random':
            # Initiate random step
            random_exp = ra(cars_dict, game_board)

            # while the red car is not yet in the right position, the algorithm goes on
            i = 0
            while cars_dict[ord('X')].position != [(2,4), (2,5)]:
                random_exp.random_step(hill_climb)
                i +=1

            # Save the amount of iterations and use it to calculate the mean
            iterations_list.append(i)
            mean_i += i
            if round % 100 == 0:
                print(f"progress:{(round/rounds) * 100}")
            round += 1

            if hill_climb and i < min_iterations:
                min_iterations = i
                min_iterations_config = copy.deepcopy(random_exp.hill_climb_config)

        elif algorithm == 'bf':
            bf_alg = bf.breadth_first_algorithm(6)
            bf_alg.search_breadth(cars_dict)

    # Calculate the mean iterations and return the list of iterations
    mean_i = mean_i/rounds
    # print (f'the mean amount of iterations over {rounds} rounds is {mean_i}')
    print ("iteration list:", iterations_list)

    if hill_climb:
        return iterations_list, min_iterations_config
    else:
        return iterations_list


def export_results_to_csv(experiment_path, results):
    
    # iterations = results
    
    with open(experiment_path, 'w') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(results)



if __name__ == '__main__':
    if not os.path.exists('results'):
        os.makedirs('results')
    
    rounds = 10
    algorithm = 'bf'

    filepath = 'data/Rushhour6x6_1.csv'
    results = game(filepath, rounds, algorithm)

    experiment_name = 'hill_climb'
    export_results_to_csv(f'results/{experiment_name}_{rounds}.csv', results)
    
    