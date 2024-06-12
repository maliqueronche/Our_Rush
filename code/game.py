import numpy as np
import pandas as pd
import classes
import board
from visualization import visualize
from user_input import user_input
from algorithm_random import Random_algorithm as ra


def game(filepath, rounds):
    """
    Takes csv file containing vehicles and adds them to game.
    Creates dictionary containing all car instances in game.
    Generates board with cars in their starting position.
    Takes input from user and makes moves based on this input.
    """
    cars = pd.read_csv(filepath)
    iterations_list = []
    mean_i = 0

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

        # Initiate random step
        random_exp = ra(cars_dict, game_board)

        # while the red car is not yet in the right position, the algorithm goes on
        i = 0
        while cars_dict[ord('X')].position != [(2,4), (2,5)]:
            random_exp.random_step()
            i +=1

        # Save the amount of iterations and use it to calculate the mean
        iterations_list.append(i)
        mean_i += i

    # Calculate the mean iterations and return the list of iterations
    mean_i = mean_i/rounds
    print (f'the mean amount of iterations over {rounds} rounds is {mean_i}')
    print (iterations_list)
    return (iterations_list)



if __name__ == '__main__':
    filepath = 'data/Rushhour6x6_1_test_red_only.csv'
    data = game(filepath, 10)
