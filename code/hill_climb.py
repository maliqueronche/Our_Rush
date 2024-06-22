from game import game
from algorithm_random import Random_algorithm as ra
import classes
import board
import random
import copy
import time
import pandas as pd


# step one: 5 random outputs
def hill_climb(filepath, slice_size, random_solutions, size):

    # compute board position for every step in random iteration, key is step, value is board position
    iterations, min_iterations_dict = game(filepath, 5, 'random', 6,  hill_climb = True)
    total_steps = len(min_iterations_dict.keys())
    # print(min_iterations_dict)
    print("total steps:", total_steps)
    # print([elem[0] for elem in min_iterations_dict.values()])
    

    # loop over slices
    for start in range(0, total_steps, slice_size):
        end = min(start + slice_size, total_steps)
        current_slice = {}

        # loop over steps in slices and index step
        for step in range(start, end):
            current_slice[step] = min_iterations_dict[step]

        best_slice = current_slice
        best_slice_steps = end - start

        for j in range(random_solutions):
            car_moves, cars_dict  = generate_random_solution(current_slice, start, end, size)
            new_steps = len(car_moves)

            if new_steps < best_slice_steps:
                best_slice = cars_dict
                best_slice_steps = new_steps
        
        keys_to_remove = list(min_iterations_dict.keys())[start:end]
        for key in keys_to_remove:
            del min_iterations_dict[key]

        # Step 4: Insert the new 300 keys into the original dictionary
        # We need to shift the original keys to make room for the new ones
        shifted_original_dict = {key + new_steps: value for key, value in min_iterations_dict.items()}

        # Merge the new dictionary with the shifted original dictionary
        final_dict = {**cars_dict, **shifted_original_dict}

        # Print the first 10 items to verify
        for key in list(final_dict.keys())[:10]:
            print(f"{key}: {final_dict[key]}")

        # for step in range(start, end):

        #     # if step - start not in best_slice:
        #     #     # print(f"Step {step - start} not in best_slice")

        #     min_iterations_dict[step] = best_slice[step - start]

    return min_iterations_dict

def generate_random_solution(current_slice, start, end, size):

    cars_dict_start = current_slice[0]
    cars_dict_end = current_slice[end]

    # create board and random instance
    game_board = board.Board(cars_dict_start, size)
    random_exp = ra(cars_dict_start, game_board)

    game_board_end = board.Board(cars_dict_end, size)

    # car positions based on current slice
    # vgm gaat het hier fout
    # for step in current_slice:
    #     for car_id, car in current_slice[step].items():
    #         cars_dict[car_id] = classes.Vehicle(car.ID, car.orientation, car.column, car.row, car.length)


        # for car_id in value:
        #     car = current_slice[step][car_id]
        #     cars_dict[car_id] = classes.Vehicle(car.ID, car.orientation, car.column, car.row, car.length)

    new_solution = {cars_dict_start}
    car_moves = []
    
    i = 0
    while i < (end - start) and new_board_end != game_board_end:
        new_board_end, car_move, cars_dict = random_exp.random_step(hill_climb = True)
        car_moves.append(car_move)
        # TODO: fix updated slice/cars dictionary for new slices
        new_solution[i] = cars_dict
        i += 1
    

    new_solution[i] = cars_dict_end
    return car_moves


if __name__ == '__main__':
    filepath = 'data/Rushhour6x6_1.csv'
    optimized_solution = hill_climb(filepath, 100, 2000, 6)
    print("solution:", len(optimized_solution.keys()))

