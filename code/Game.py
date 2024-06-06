import numpy as np
import pandas as pd
import Classes
import board
from visualization import visualize



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

    #visualize starting point
    visualize(cars_dict)

    keep_playing = True
    while keep_playing:
        move_input = input("Enter move (ID direction) or 'q' to quit: ").split()

        
        if move_input[0].lower() == 'q':
            keep_playing = False
        elif len(move_input) != 2:
            print("Invalid input. Enter move as 'ID direction' or 'q' to quit.")
        else:
            move_id, direction = move_input
            if not move_id.isdigit():
                print("Invalid ID. ID should be a number.")
            else:
                ID = int(move_id)
                if direction.lower() not in ['left', 'right', 'up', 'down']:
                    print("Invalid direction. Use 'left', 'right', 'up', or 'down'.")
                else:
                    game_board.one_move(ID, direction.lower())
                    visualize(cars_dict)



    print (game_board)
    visualize(cars_dict)



if __name__ == '__main__':
    filepath = 'data/Rushhour6x6_1.csv'
    game(filepath)
