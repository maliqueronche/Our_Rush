from run_random_algorithm import run_random
from algorithm_random import Random_algorithm as ra
import classes
import board
import random
import copy
import time
import pandas as pd
from pprint import pprint



class hillclimb():
    # step one: 5 random outputs

    def __init__(self, size):
        self.size = size


    def hc_alg(self, filepath, end_position):

        # compute board position for every step in random iteration, key is step, value is board position
        min_iterations_dict = run_random(filepath, 10, 'random', self.size, end_position, hill_climb = True)
        total_steps = len(min_iterations_dict.keys())
        slice_size = 200
        random_solutions = 100
        loop_rounds = 10
        hill_climb_solution = {}
        print("first key and value:", min_iterations_dict.get(0, 'Key 1 not found'))
        print("200th key and value:", min_iterations_dict.get(199, 'Key 200 not found'))
        print("total steps:", total_steps)
        
        # loop over rounds
        # print("first key and value:", min_iterations_dict.get(0, 'Key 1 not found'))
        # print("200th key and value:", min_iterations_dict.get(199, 'Key 200 not found'))
        # print("total steps:", total_steps)
        
            
        # loop over slices
        for start in range(0, total_steps, slice_size):
            # print("begin of the slice:", start, "steps:", len(min_iterations_dict.keys()))
            end = min(start + slice_size, total_steps)
            # print("end", end)
            current_slice = {step: min_iterations_dict[step] for step in range(start, end)}
            
            # before_slice_start = current_slice[start]
            # game_board_before_start = board.Board(before_slice_start, size)

            # print("before slice slice")
            # print(game_board_before_start.board)
            # before_slice_end = current_slice[(len(current_slice)+start-1)]
            # game_board_before_end = board.Board(before_slice_end, size)
            # print(game_board_before_end.board)


            if not current_slice:
                print(f"No steps found in range {start}-{end}. Skipping this slice.")
                continue

            best_slice = current_slice
            best_slice_steps = end - start

            for _ in range(random_solutions):
                
                car_moves, new_solution  = self.generate_random_solution(current_slice, start, end)
                if len(car_moves) < best_slice_steps and len(car_moves) != 0:
                    
                    # print(len(new_solution.keys()))
                    # print("created best slice")
                    
                    best_slice = copy.deepcopy(new_solution)
                    
                    
                    best_slice_steps = len(car_moves)
            
            # print("start", start)
            # after_slice_start = best_slice[start]
            # game_board_after_start = board.Board(after_slice_start, size)

            # print("\nafter slice")
            # print(game_board_after_start.board)
            # after_slice_end = best_slice[(len(best_slice)+start-1)]
            # game_board_after_end = board.Board(after_slice_end, size)

            
            # print(game_board_after_end.board)
            hill_climb_solution.update(best_slice)
            # print("length hillclimb solution", len(hill_climb_solution.keys()))
            
                        
            
            # print(len(hill_climb_solution.keys()))
            # pprint(hill_climb_solution)
            
        return car_moves

    def generate_random_solution(self, current_slice, start, end):
        if start not in current_slice or end - 1 not in current_slice:
            print(f"Error: Missing start ({start}) or end-1 ({end-1}) key in current_slice")
            return [], current_slice

        # Indexing start and end board of current slice
        intermediate_slice = copy.deepcopy(current_slice)

        cars_dict_start = intermediate_slice[start]
        cars_dict_end = intermediate_slice[end-1]

        new_cars_dict = {}
        for car_id, car in cars_dict_start.items():
            position_car = car.position
            orientation_car = car.orientation
            new_cars_dict[car_id] = {'id' : car_id, 'position' : position_car, 'orientation': orientation_car}

        # create board and random instance
        game_board_start = board.Board(new_cars_dict, self.size)
        # print("game_board_Start_intermediate", game_board_start.board)
        game_board_end = board.Board(cars_dict_end, self.size)
        # print(game_board_start.board, game_board_end.board)
        # random_exp = ra(cars_dict_start, game_board_start)
        

        new_solution = {}
        new_solution[start] = new_cars_dict
        intermediate_start = start
        car_moves = []
        new_board_end = game_board_start
        start += 1
        
        new_cars_dict = copy.deepcopy(new_cars_dict)

        while start < end and (new_board_end.board != game_board_end.board).any():
            
            new_board_end, car_move, cars_dict = self.random_step_hc(new_cars_dict, new_board_end)
            # print(new_board_end.board)
            
            # print(f"Attempting move {car_move} at step {i}")
            # print(f"Board state after move {i}:\n{new_board_end.board}")
            car_moves.append(car_move)
            new_solution[start] = new_cars_dict
            start += 1
            new_cars_dict = copy.deepcopy(cars_dict)
        

            # print("i", i)
        game_board_before_return = board.Board(new_solution[intermediate_start], size)
        # print("game_board_Start_intermediatafter", game_board_before_return.board)

        if start < end and (new_board_end.board != game_board_end.board).any():
            return car_moves, new_solution
        else:
            empty_car_moves = []
            return empty_car_moves, current_slice
        

    def get_available_cars(self, cars_dict, board):
        available_cars = {}

        for car_id, car in cars_dict.items():
            moveable_list = self.is_moveable(car, board)
            if True in moveable_list:
                available_cars[car_id] = car
        return available_cars


    def get_new_pos(self, car_tup, direction, orientation):
        '''recieves a tuple for location and a direction and moves the tuple one place'''
        row, col = car_tup

        if orientation == 'H':
            if direction == 'pos':
                col +=1
            elif direction == 'neg':
                col -= 1
        elif orientation == 'V':
            if direction == 'pos':
                row +=1
            elif direction == 'neg':
                row -= 1

        return row, col
        

    def is_moveable(self, car, board):

        position = car['position']
        orientation = car['orientation']
        positions_to_check = []
        checklist = []

        neg_pos = self.get_new_pos(position[0], 'neg', orientation)
        positions_to_check.append(neg_pos)

        pos_pos = self.get_new_pos(position[-1], 'pos', orientation)
        positions_to_check.append(pos_pos)

        for row, col in positions_to_check:
            position = row, col
            if row > self.size -1 or row <0 or col > self.size -1 or col <0:
                checklist.append(False)
            elif board.board[position] == 0:
                checklist.append(True)
            else:
                checklist.append(False)
        return checklist
    
    def get_random_car(self, cars_dict):
        """Choose a random car from cars"""
        
        key = random.choice(list(cars_dict.keys()))
        
        return key, cars_dict[key]

    def random_step_hc(self, new_cars_dict, board): #dictionary and board instance
            """Does a random step for a random moveable vehicle and returns the updated board."""

            # Get dictionary with available cars (i.e. moveable)
            pick = self.get_available_cars(new_cars_dict, board)
            
            # Get a random car and get moveable directions
            car_id, car = self.get_random_car(pick)
            # self.car = car
            # self.car_id = car_id
            
            moveable_list = self.is_moveable(car, board)
            

            # Pick a random direction (backwards (0) or forwards(1)) and move the car
            direction = random.randint(0,1)
            new_position = []
            # If backwards, move car left or up, else right or down, 
            if direction == 0: 
                if moveable_list[0] == True:
                    for car_tup in car['position']:
                        new_pos = self.get_new_pos(car_tup, 'neg', car['orientation'])
                        new_position.append(new_pos)
                    car['position'] = new_position
                    # if hill_climb:   
                    car_move = (car_id, '-1')
                    new_board = board.Board(new_cars_dict, self.size)
                else:
                    for car_tup in car['position']:
                        new_pos = self.get_new_pos(car_tup, 'pos', car['orientation'])
                        new_position.append(new_pos)
                    car['position'] = new_position
                    # if hill_climb:
                    car_move = (car_id, '1')
                    new_board = board.Board(new_cars_dict, self.size)
                    
            # Elif forwards, move car right or down, else left or up
            elif direction == 1:
                if moveable_list[1] == True:
                    for car_tup in car['position']:
                        new_pos = self.get_new_pos(car_tup, 'pos', car['orientation'])
                        new_position.append(new_pos)
                    car['position'] = new_position
                    car_move = (car_id, '1')
                    new_board = board.Board(new_cars_dict, self.size)
                else:
                    for car_tup in car['position']:
                        new_pos = self.get_new_pos(car_tup, 'neg', car['orientation'])
                        new_position.append(new_pos)
                    car['position'] = new_position
                    car_move = (car_id, '-1')
                    new_board = board.Board(new_cars_dict, self.size)
            

            
            return new_board, car_move, cars_dict
            

if __name__ == '__main__':
    filepath = 'data/Rushhour6x6_1.csv'
    car_moves = hc_alg(filepath, 200, 100, 6)
    print("solution:", len(optimized_solution.keys()))

    
   
