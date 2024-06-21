from game import game
from algorithm_random import Random_algorithm as ra
import classes
import board
import random
import copy
import time
import pandas as pd


# step one: 5 random outputs
def hill_climb(filepath, slice_size, random_solutions):

    # compute board position for every step in random iteration, key is step, value is board position
    iterations, min_iterations_dict = game(filepath, 5, 'random', 6,  hill_climb = True)
    total_steps = len(min_iterations_dict.keys())
    print(min_iterations_dict)
    print("total steps:", total_steps)
    # print([elem[0] for elem in min_iterations_dict.values()])
    

    # loop over slices
    for start in range(0, total_steps, slice_size):
        end = min(start + slice_size, total_steps)
        current_slice = {}

        # go in the slice
        for step in range(start, end):

            # if step not in min_iterations_dict:
            #     # print(f"Step {step} not in min_iterations_dict")
            #     continue  
            # print(f"Step {step} in min_iterations_dict")

            current_slice[step] = min_iterations_dict[step]

            best_slice = current_slice
            best_slice_steps = end - step

            for j in range(random_solutions):
                random_solution = generate_random_solution(filepath, current_slice, start, end)
                new_steps = len(random_solution)

                if new_steps < best_slice_steps:
                    best_slice = random_solution
                    best_slice_steps = new_steps

            for step in range(start, end):

                # if step - start not in best_slice:
                #     # print(f"Step {step - start} not in best_slice")

                min_iterations_dict[step] = best_slice[step - start]

    return min_iterations_dict

def generate_random_solution(filepath, current_slice, start, end):

    cars = pd.read_csv(filepath)
    cars_dict = {}

    for index, row in cars.iterrows():
        ID = 0
        for i in row['car']:
            ID += ord(i)
        vehicle = classes.Vehicle(ID, row['orientation'], row['col'], row['row'], row['length'])
        cars_dict[ID] = vehicle
    
    # create board and random instance
    game_board = board.Board(cars_dict, size = 6)
    random_exp = ra(cars_dict, game_board)

    # car positions based on current slice
    # vgm gaat het hier fout
    for step, value in current_slice.iterrows():
        for car_id in value:
            car = current_slice[step][car_id]
            cars_dict[car_id] = classes.Vehicle(car.ID, car.orientation, car.column, car.row, car.length)

    new_solution = {}
    i = 0
    while i < (end - start) and cars_dict[ord('X')].position != [(2, 4), (2, 5)]:
        random_exp.random_step(hill_climb = True)
        new_solution[i] = random_exp.copy_cars_dict(cars_dict)
        i += 1
    
    return new_solution


if __name__ == '__main__':
    filepath = 'data/Rushhour6x6_1.csv'
    optimized_solution = hill_climb(filepath, 100, 2000 )
    print("solution:", len(optimized_solution.keys()))

