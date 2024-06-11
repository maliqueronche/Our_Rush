import numpy as np
import pandas as pd
import classes
import board
from visualization import visualize
from user_input import user_input
from algorithm_random import Random_algorithm as ra


def game(filepath):
    """
    Takes csv file containing vehicles and adds them to game.
    Creates dictionary containing all car instances in game.
    Generates board with cars in their starting position.
    Takes input from user and makes moves based on this input.
    """
    cars = pd.read_csv(filepath)
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

    # Visualize starting point
    # visualize(cars_dict, game_board)

    # Initiate random step
    random_exp = ra(cars_dict, game_board)

    # while the red car is not yet in the right position, the algorithm goes on
    i = 0
    # while cars_dict[ord('X')] != ((2,4), (2,5)):
    while i <= 6:
        random_exp.random_step()

        i +=1



if __name__ == '__main__':
    filepath = 'data/Rushhour6x6_1.csv'
    game(filepath)
