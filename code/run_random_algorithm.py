from algorithm_random import Random_algorithm as ra
import pandas as pd
import numpy as np
import board
import classes
from time import time

def run_random(filepath, rounds, algorithm, size, end_position):
    """
    Executes the Random Algorithm for a specified number of rounds.

    Args:
        filepath (str): Path to the CSV file containing car information.
        rounds (int): Number of rounds to run the algorithm.
        algorithm (str): The algorithm to use ('random').
        size (int): The size of the board.
        end_position (tuple): The target end position for the red car.

    Returns a list of car moves.
    """

    cars = pd.read_csv(filepath) 
    car_moves = []

    # initialize start time
    start = time()

    for round in range(rounds):
        
        cars_dict = {}

        # loop over cars dataframe, create vehicles and store them in dictionary
        for idx, row in cars.iterrows():
            ID = sum(ord(letter) for letter in row['car'])
            vehicle = classes.Vehicle(ID, row['orientation'], row['col'], row['row'], row['length'])
            cars_dict[ID] = vehicle

        # initialise board and add cars in starting positions
        game_board = board.Board(cars_dict, size)
    
        if algorithm == 'random':

            # initiate random step
            random_exp = ra(cars_dict, game_board)
            i = 0

            while cars_dict[ord('X')].position != end_position:
                car_moves.append(random_exp.random_step())
                i +=1
                
            if round % 100 == 0:
                end = time()
                print(f'The time elapsed: {end-start:.2f} seconds.')
                print(f"progress:{(round/rounds) * 100}")
                start = time()
            
    return car_moves


