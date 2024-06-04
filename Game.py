import numpy as np
import pandas as pd
import Classes
import board



def game(filepath):
    """
    Takes a csv file containing vehicles and adds them to the game.
    """
    cars = pd.read_csv(filepath)
    cars_dict = {}
    print (cars)

    # Loop over cars dataframe, create vehicles and store them in a dictionary
    for idx, row in cars.iterrows():
        print (row['car'])
        ID = ord(row['car'])
        vehicle = Classes.Vehicle(ID, row['orientation'], row['col'], row['row'], row['length'])
        cars_dict[ID] = vehicle

    # Initialise board and add cars in starting positions
    game_board = board.Board()
    game_board.place_cars(cars_dict)

    # Move cars
    game_board.one_move(88)
    game_board.one_move(74)
    
    print (game_board)
        



if __name__ == '__main__':
    filepath = 'Rushhour6x6_1.csv'
    game(filepath)
    