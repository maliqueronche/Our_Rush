from run_random_algorithm import run_random
from algorithm_random import Random_algorithm as ra
import classes
import board
import random
import copy
import time
import pandas as pd
from pprint import pprint



# step one: 5 random outputs
def hc_alg(filepath, end_position, size):

    # compute board position for every step in random iteration, key is step, value is board position
    min_iterations_dict = run_random(filepath, 10, 'random', size, end_position, hill_climb = True)
    total_steps = len(min_iterations_dict.keys())
    slice_size = 200
    random_solutions = 100
    loop_rounds = 10
    hill_climb_solution = {}
    print("first key and value:", min_iterations_dict.get(0, 'Key 1 not found'))
    print("200th key and value:", min_iterations_dict.get(199, 'Key 200 not found'))
    print("total steps:", total_steps)
    
    # loop over rounds
    car_moves = []
    
        
    # loop over slices
    for start in range(0, total_steps, slice_size):
        print("begin of the slice:", start, "steps:", len(min_iterations_dict.keys()))
        end = min(start + slice_size, total_steps)
        current_slice = {step: min_iterations_dict[step] for step in range(start, end)}

        if not current_slice:
            print(f"No steps found in range {start}-{end}. Skipping this slice.")
            continue

        best_slice = current_slice
        best_slice_steps = end - start
        

        for _ in range(random_solutions):
            
            car_moves, new_solution = generate_random_solution(current_slice, start, end, size)
            
            if len(car_moves) < best_slice_steps:
                
                print(len(new_solution.keys()))
                print("created best slice")
                best_slice = new_solution
                best_slice_steps = len(car_moves)
            
            
        hill_climb_solution.update(best_slice)
        print("length hillclimb solution", len(hill_climb_solution.keys()))
        
        
        
        
        print(len(hill_climb_solution.keys()))
        pprint(hill_climb_solution)
    return car_moves

def generate_random_solution(current_slice, start, end, size):
    if start not in current_slice or end - 1 not in current_slice:
        print(f"Error: Missing start ({start}) or end-1 ({end-1}) key in current_slice")
        return [], current_slice

    # Indexing start and end board of current slice
    intermediate_slice = copy.deepcopy(current_slice)

    cars_dict_start = intermediate_slice[start]
    cars_dict_end = intermediate_slice[end-1]

    # create board and random instance
    game_board_start = board.Board(cars_dict_start, size)
    game_board_end = board.Board(cars_dict_end, size)
    random_exp = ra(cars_dict_start, game_board_start)

    new_solution = {}
    car_moves = []
    new_board_end = game_board_start
    i = 0
    
 
    while i < (end - start) and (new_board_end.board != game_board_end.board).any():
    # while (new_board_end.board != game_board_end.board).any():
        new_board_end, car_move, cars_dict = random_exp.random_step(hill_climb = True)
        car_moves.append(car_move)
        
        # TODO: fix updated slice/cars dictionary for new slices
        new_solution[i] = cars_dict
        i += 1

        # print("i", i)
    
    
    

    
    return car_moves, new_solution
    


if __name__ == '__main__':
    filepath = 'data/Rushhour6x6_1.csv'
    car_moves = hc_alg(filepath, 200, 100, 6)
    print("solution:", len(optimized_solution.keys()))

    
   
