import numpy as np
import pandas as pd
import Classes
import board



def game(filepath):
    cars = pd.read_csv(filepath)
    cars_dict = {}
    print (cars)

    for idx, row in cars.iterrows():
        print (row['car'])
        ID = ord(row['car'])
        vehicle = Classes.Vehicle(ID, row['orientation'], row['col'], row['row'], row['length'])
        cars_dict[ID] = vehicle

    game_board = board.Board()
    game_board.place_cars(cars_dict)

    game_board.one_move()
    
    print (game_board)
        



if __name__ == '__main__':
    filepath = '/home/malique/Our_Rush/Rushhour6x6_1.csv'
    game(filepath)
    