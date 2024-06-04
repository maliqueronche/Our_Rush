import pandas as pd
import Classes
import Board



def game(filepath):
    cars = pd.read_csv(filepath)
    display (cars)

    for car in cars:
        car = Vehicle(cars[orientation, col, row, length])
    