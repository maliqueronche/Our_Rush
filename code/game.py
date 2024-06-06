import numpy as np
import pandas as pd
import classes
import board
from visualization import visualize



def game(filepath):
    """
    Takes a csv file containing vehicles and adds them to the game.
    Creates dictionary containing all car instances in the game.
    Generates board with cars in their starting position.
    Takes input from user and makes moves based on this input.
    """
    cars = pd.read_csv(filepath)
    cars_dict = {}
    print (cars)

    # Loop over cars dataframe, create vehicles and store them in dictionary
    for idx, row in cars.iterrows():
        ID = ord(row['car'])
        vehicle = classes.Vehicle(ID, row['orientation'], row['col'], row['row'], row['length'])
        cars_dict[ID] = vehicle

    # Initialise board and add cars in starting positions
    game_board = board.Board()
    game_board.place_cars(cars_dict)

    # Visualize starting point
    visualize(cars_dict, game_board)

    # Ask for user input and keep playing until user quits
    keep_playing = True
    while keep_playing:
        move_input = input("Enter move (ID direction) or 'q' to quit: ").split()
        if len(move_input) == 1 and move_input[0].lower() == 'q':
            keep_playing = False

        # If input is correctly formatted, make a move
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
                    visualize(cars_dict, game_board)


if __name__ == '__main__':
    filepath = 'data/Rushhour6x6_1.csv'
<<<<<<< HEAD
    game(filepath)
=======
    game(filepath)
>>>>>>> 9887ff64c4aace3472bc2c7816276206d764faa7
