from run_random_algorithm import run_random
from algorithm_random import Random_algorithm as ra
import classes
import board
import random
import copy
import time
import pandas as pd
from pprint import pprint
from helpers import export_hillclimber_to_csv



# step one: 5 random outputs
def hc_alg(filepath, end_position, size):

    # compute board position for every step in random iteration, key is step, value is board position
    min_iterations_dict = run_random(filepath, 10, 'random', size, end_position, hill_climb = True)
    total_steps = len(min_iterations_dict.keys())
    slice_size = 200
    random_solutions = 10
    loop_rounds = 10
    hill_climb_solution = {}
    print("first key and value:", min_iterations_dict.get(0, 'Key 1 not found'))
    print("200th key and value:", min_iterations_dict.get(199, 'Key 200 not found'))
    print("total steps:", total_steps)
    car_moves = []
    # loop over rounds
    # print("first key and value:", min_iterations_dict.get(0, 'Key 1 not found'))
    # print("200th key and value:", min_iterations_dict.get(199, 'Key 200 not found'))
    # print("total steps:", total_steps)
    
        
    # loop over slices
    for start in range(0, total_steps, slice_size):
        print("begin of the slice:", start, "steps:", len(min_iterations_dict.keys()))
        end = min(start + slice_size, total_steps)
        print("end", end)
        current_slice = {step: min_iterations_dict[step] for step in range(start, end)}
        
        before_slice_start = current_slice[start]
        game_board_before_start = board.Board(before_slice_start, size)

        print("before slice slice")
        print(game_board_before_start.board)
        before_slice_end = current_slice[(len(current_slice)+start-1)]
        game_board_before_end = board.Board(before_slice_end, size)
        print(game_board_before_end.board)


        if not current_slice:
            print(f"No steps found in range {start}-{end}. Skipping this slice.")
            continue

        best_slice = current_slice
        best_slice_steps = end - start

        for _ in range(random_solutions):
            
            # car_moves, new_solution = generate_random_solution(current_slice, start, end, size)
            
            car_moves, new_solution  = generate_random_solution(current_slice, start, end, size)
            if len(car_moves) < best_slice_steps and len(car_moves) != 0:
                
                # print(len(new_solution.keys()))
                # print("created best slice")
                
                best_slice = copy.deepcopy(new_solution)
                
                
                best_slice_steps = len(car_moves)
        
        print("start", start)
        after_slice_start = best_slice[start]
        game_board_after_start = board.Board(after_slice_start, size)

        print("\nafter slice")
        print(game_board_after_start.board)
        after_slice_end = best_slice[(len(best_slice)+start-1)]
        game_board_after_end = board.Board(after_slice_end, size)

        
        print(game_board_after_end.board)
        hill_climb_solution.update(best_slice)
        # print("length hillclimb solution", len(hill_climb_solution.keys()))
        
                    
        
        # print(len(hill_climb_solution.keys()))
        # pprint(hill_climb_solution)
        
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
    print("game_board_Start_intermediate", game_board_start.board)
    game_board_end = board.Board(cars_dict_end, size)
    # print(game_board_start.board, game_board_end.board)
    random_exp = ra(cars_dict_start, game_board_start)
    

    new_solution = {}
    new_solution[start] = cars_dict_start
    intermediate_start = start
    car_moves = []
    new_board_end = game_board_start
    start += 1
 


    while start < end and (new_board_end.board != game_board_end.board).any():
    # while (new_board_end.board != game_board_end.board).any():
        new_board_end, car_move, cars_dict = random_exp.random_step(hill_climb = True)
        # print(new_board_end.board)
        
        # print(f"Attempting move {car_move} at step {i}")
        # print(f"Board state after move {i}:\n{new_board_end.board}")
        
        new_cars_dict = copy.deepcopy(cars_dict)
        car_moves.append(car_move)
        new_solution[start] = new_cars_dict
        start += 1

        # print("i", i)
    game_board_before_return = board.Board(new_solution[intermediate_start], size)
    print("game_board_Start_intermediatafter", game_board_before_return.board)
    return car_moves, new_solution
    

    

if __name__ == '__main__':
    filepath = 'data/Rushhour6x6_1_test_red_only.csv'
    car_moves = hc_alg('data/Rushhour6x6_1_test_red_only.csv', [(2, 4), (2, 5)], 6)
    print("solution:", car_moves)
    experiment_name = "test_hillclimb"
    export_hillclimber_to_csv(f'results/{experiment_name}.csv', car_moves)
    
   
