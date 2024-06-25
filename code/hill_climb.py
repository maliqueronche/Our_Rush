from run_random_algorithm import run_random
from algorithm_random import Random_algorithm as ra
import classes
import board
import random
import copy
import time
import pandas as pd
import numpy as np
from pprint import pprint
from helpers import export_hillclimber_to_csv
from animation import animate

class hill_climber():

    def __init__(self, filepath, end_position, size):
        self.list_of_cars = pd.read_csv(filepath, index_col = 'car') 
        self.size = size
        self.end_position = end_position
        
        # Loop over cars dataframe, create vehicles and store them in dictionary
        cars_dict = self.list_to_cars_dict(self.list_of_cars)

        #self.cars_pos_and_ori = cars_pos_and_ori
        self.start_cars_dict = cars_dict
        self.start_board = board.Board(cars_dict, size)
        
    def run_hc(self):
        best_steps = []
        random_steps = {}
        while len(random_steps) == 0:
            random_steps = self.get_random_steps(self.start_board,self.start_cars_dict)
            
        shortest_moves = {}

        current_cars_dict = copy.deepcopy(self.start_cars_dict)
        current_list_of_cars = copy.deepcopy(self.list_of_cars)
    
        start_pos = 0
        for end_pos in range(0, len(random_steps), 500):
            start_position_shortest_moves = len(shortest_moves)
            print (end_pos)
            if end_pos != 0:
                print(end_pos)
                difference = end_pos - start_pos
            
                board1 = copy.deepcopy(random_steps[start_pos]['car_move'])
                board2 = copy.deepcopy(random_steps[end_pos]['car_move'])
                shortest_path, car_moves = self.find_shortest_path(board1, board2,current_cars_dict, current_list_of_cars, difference)
                # print ('shortest path:')
                # print (shortest_path)

                # print ('car_moves')
                # print (car_moves)

                for idx, game_board in car_moves['moves'].items():
                    # print (start_position_shortest_moves, idx)
                    shortest_moves[start_position_shortest_moves + idx] = game_board

                # print (car_moves['steps'])
                for car_step in car_moves['steps']:
                    best_steps.append(car_step)

            start_pos = end_pos

        print ('shortest moves:')
        print (shortest_moves)

        print ('steps')
        print (best_steps)
        return best_steps

    def list_to_cars_dict(self, list_of_cars):
        cars_dict = {}
        cars_pos_and_ori = {}
        for idx, row in list_of_cars.iterrows():
            ID = 0
            for letter in idx:
                ID += ord(idx)
            vehicle = classes.Vehicle(ID, row['orientation'], row['col'], row['row'], row['length'])
            cars_pos_and_ori[ID] = vehicle.position, vehicle.orientation
            cars_dict[ID] = vehicle
        return cars_dict

    def find_shortest_path(self, board1, board2, cars_dict, list_of_cars, difference):
        fastest_path = difference
        top_10_rounds = {}
        current_board = copy.deepcopy(board1)
        end_board = copy.deepcopy(board2)
        cars_dict = copy.deepcopy(cars_dict)

        print (current_board)

        for i in range (10):
            print(i)
            current_steps = []
            shorter_random_steps = {}

            while not np.array_equal(current_board, end_board):
                info = self.one_path_round(current_steps, fastest_path, current_board, cars_dict, list_of_cars)

                car_move, list_of_cars, step = info
                

                shorter_random_steps[len(current_steps)] = car_move
                current_steps.append(step)

                current_board = copy.deepcopy(car_move)

            current_board = copy.deepcopy(board1)
            end_board = copy.deepcopy(board2)
            print (current_steps)   
            if len(current_steps) <= fastest_path:
                top_10_rounds[len(current_steps)] = {'moves':shorter_random_steps, 'steps':current_steps}

        sorted_list = sorted(top_10_rounds.items())
        return sorted_list[0]

    def one_path_round(self, current_steps, fastest_path, current_board, cars_dict, list_of_cars):

        list_of_cars = copy.deepcopy(list_of_cars)
        current_board = board.Board(cars_dict, self.size)
        car_move, list_of_cars, step = self.one_random_step(current_board, cars_dict, list_of_cars)

        if len(current_steps) >= 1:
            while step[0] == current_steps[-1][0]:
                list_of_cars = copy.deepcopy(list_of_cars)
                current_board = board.Board(cars_dict, self.size)
                car_move, list_of_cars, step = self.one_random_step(current_board, cars_dict, list_of_cars)

        return car_move, list_of_cars, step

    def get_random_steps(self, board, cars_dict):
        steps_dict = {}
        step_count = 0
        red_car_position = cars_dict[ord('X')].position
        list_of_cars = self.list_of_cars

        while red_car_position != self.end_position:
            
            car_move, list_of_cars, step = self.one_random_step(board, cars_dict, list_of_cars)

            steps_dict[step_count] = {'car_move':car_move, 'list_of_cars':list_of_cars}
            red_car_position = cars_dict[ord('X')].position
            step_count +=1
            if step_count >= 5000:
                return {}
        return steps_dict
            
    def one_random_step(self, board, cars_dict, list_of_cars):
        available_cars = self.get_available_cars(cars_dict, board)
        car_id, car = self.get_random_car(available_cars)
        moveable_list = self.is_moveable(car, board)

        direction = random.randint(0,1)

        if direction == 0:
            if moveable_list[0] == True:
                car_move, list_of_cars, step = self.move_car(direction, board, car_id, car, list_of_cars)
            else :
                direction = 1
                car_move, list_of_cars, step = self.move_car(direction, board, car_id, car, list_of_cars)
        elif direction == 1:
            if moveable_list[1] == True:
                car_move, list_of_cars, step = self.move_car(direction, board, car_id, car, list_of_cars)
            else:
                direction = 0
                car_move, list_of_cars, step = self.move_car(direction, board, car_id, car, list_of_cars)
        
        return car_move, list_of_cars, step

    def get_random_car(self, cars_dict):
        """Choose a random car from cars"""
        
        key = random.choice(list(cars_dict.keys()))
        
        return key, cars_dict[key]
    
    def get_available_cars(self, cars_dict, board):
        """"For every car in cars, if it is moveable, add the car to available cars and return that dictionary."""

        available_cars = {}

        # Loop over cars, check if a car can move and add it to dictionary
        for car_id in cars_dict.keys():
            
            moveable_list = self.is_moveable(cars_dict[car_id], board)
            
            if True in moveable_list:
                available_cars[car_id] = cars_dict[car_id]
                
        return available_cars

    def is_moveable(self, car, board):
        """Takes a car, checks if it can move and returns list with tuples containing True or False."""

        positions_list = car.position
        orientation = car.orientation
        self.orientation = orientation
        positions_to_check = []
        checklist = []

        # Get positions to check 
        neg_pos = board.get_new_pos(positions_list[0], 'neg', orientation)
        positions_to_check.append(neg_pos)
        pos_pos = board.get_new_pos(positions_list[-1], 'pos', orientation)
        positions_to_check.append(pos_pos)
        
        # Check if position can be moved to
        for row, col in positions_to_check:
                position = row, col
                if row > board.size -1 or row <0 or col > board.size -1 or col <0:
                    checklist.append(False)
                elif board.board[position] == 0:
                    checklist.append(True)
                else:
                    checklist.append(False)
        return checklist

    def move_car(self, direction, board, car_id, car, list_of_cars):
        if direction == 0:
            board.move_car(car_id, 'neg')
            car.change_position('neg', car.orientation)
            current_board = copy.deepcopy(board.board)
            list_of_cars = self.get_new_list_of_cars(list_of_cars, direction, car_id)
            step = car_id, '-1'
        if direction == 1:
            board.move_car(car_id, 'pos')
            car.change_position('pos', car.orientation)
            current_board = copy.deepcopy(board.board)
            list_of_cars = self.get_new_list_of_cars(list_of_cars, direction, car_id)
            step = car_id, '1'
        return current_board, list_of_cars, step

    def get_new_list_of_cars(self, list_of_cars, direction, car_id):
        list_of_cars = copy.deepcopy(list_of_cars)
        if direction == 0:
            if list_of_cars.loc[chr(car_id), 'orientation'] == 'H':
                list_of_cars.loc[chr(car_id), 'col'] -= 1
            else:
                list_of_cars.loc[chr(car_id), 'row'] -= 1
        elif direction == 1:
            if list_of_cars.loc[chr(car_id), 'orientation'] == 'H':
                list_of_cars.loc[chr(car_id), 'col'] += 1
            else:
                list_of_cars.loc[chr(car_id), 'row'] += 1

        return list_of_cars



        


# class hillclimb():
#     # step one: 5 random outputs

#     def __init__(self, size):
#         self.size = size


#     def hc_alg(self, filepath, end_position):

#         # compute board position for every step in random iteration, key is step, value is board position
#         min_iterations_dict, car_moves = run_random(filepath, 10, 'random', self.size, end_position, hill_climb = True)
#         print(car_moves)
#         total_steps = len(min_iterations_dict.keys())
#         slice_size = 200
#         random_solutions = 10
#         loop_rounds = 10
#         hill_climb_solution = {}
#         print("first key and value:", min_iterations_dict.get(0, 'Key 1 not found'))
#         print("200th key and value:", min_iterations_dict.get(199, 'Key 200 not found'))
#         print("total steps:", total_steps)
        
#         # loop over rounds
#         # print("first key and value:", min_iterations_dict.get(0, 'Key 1 not found'))
#         # print("200th key and value:", min_iterations_dict.get(199, 'Key 200 not found'))
#         # print("total steps:", total_steps)
#         hillclimb_car_moves = []
            
#         # loop over slices
#         for start in range(0, total_steps, slice_size):
#             # print("begin of the slice:", start, "steps:", len(min_iterations_dict.keys()))
#             end = min(start + slice_size, total_steps)
#             # print("end", end)
#             current_slice = {step: min_iterations_dict[step] for step in range(start, end)}
#             current_moves_slice = car_moves[start:end]
#             print(current_moves_slice)
#             # before_slice_start = current_slice[start]
#             # game_board_before_start = board.Board(before_slice_start, size)

#             # print("before slice slice")
#             # print(game_board_before_start.board)
#             # before_slice_end = current_slice[(len(current_slice)+start-1)]
#             # game_board_before_end = board.Board(before_slice_end, size)
#             # print(game_board_before_end.board)


#             if not current_slice:
#                 print(f"No steps found in range {start}-{end}. Skipping this slice.")
#                 continue

#             best_slice = current_slice
#             best_slice_steps = end - start

#             for _ in range(random_solutions):
                
#                 in_between_car_moves, new_solution  = self.generate_random_solution(current_slice, start, end, hillclimb_car_moves, current_moves_slice)
#                 if len(in_between_car_moves) < best_slice_steps and len(in_between_car_moves) != 0:
                    
#                     # print(len(new_solution.keys()))
#                     # print("created best slice")
#                     hillclimb_car_moves = in_between_car_moves
#                     best_slice = copy.deepcopy(new_solution)
                    
                    
#                     best_slice_steps = len(hillclimb_car_moves)
            
#             # print("start", start)
#             # after_slice_start = best_slice[start]
#             # game_board_after_start = board.Board(after_slice_start, size)

#             # print("\nafter slice")
#             # print(game_board_after_start.board)
#             # after_slice_end = best_slice[(len(best_slice)+start-1)]
#             # game_board_after_end = board.Board(after_slice_end, size)

            
#             # print(game_board_after_end.board)
#             hill_climb_solution.update(best_slice)
#             # print("length hillclimb solution", len(hill_climb_solution.keys()))
            
                        
            
#             # print(len(hill_climb_solution.keys()))
#             # pprint(hill_climb_solution)
            
#         return hillclimb_car_moves

#     def generate_random_solution(self, current_slice, start, end, car_moves, current_moves_slice):
#         if start not in current_slice or end - 1 not in current_slice:
#             print(f"Error: Missing start ({start}) or end-1 ({end-1}) key in current_slice")
#             return [], current_slice

#         # Indexing start and end board of current slice
#         intermediate_slice = copy.deepcopy(current_slice)

#         cars_dict_start = intermediate_slice[start]
#         cars_dict_end = intermediate_slice[end-1]

#         new_cars_dict = {}
#         for car_id, car in cars_dict_start.items():
#             position_car = car.position
#             orientation_car = car.orientation
#             new_cars_dict[car_id] = {'id' : car_id, 'position' : position_car, 'orientation': orientation_car}

#         # create board and random instance
#         game_board_start = brd.Board(new_cars_dict, self.size)
#         # print("game_board_Start_intermediate", game_board_start.board)
#         game_board_end = brd.Board(cars_dict_end, self.size)
#         # print(game_board_start.board, game_board_end.board)
#         # random_exp = ra(cars_dict_start, game_board_start)
        

#         new_solution = {}
#         new_solution[start] = new_cars_dict
#         intermediate_start = start
        
#         new_board_end = game_board_start
#         start += 1
        
#         new_cars_dict = copy.deepcopy(new_cars_dict)

#         while start < end and (new_board_end.board != game_board_end.board).any():
            
#             new_board_end, car_move, cars_dict = self.random_step_hc(new_cars_dict, new_board_end)
#             # print(new_board_end.board)
            
#             # print(f"Attempting move {car_move} at step {i}")
#             # print(f"Board state after move {i}:\n{new_board_end.board}")
#             car_moves.append(car_move)
#             new_solution[start] = cars_dict
#             start += 1
#             new_cars_dict = copy.deepcopy(cars_dict)
        

#             # print("i", i)
#         # game_board_before_return = board.Board(new_solution[intermediate_start], size)
#         # print("game_board_Start_intermediatafter", game_board_before_return.board)

#         if start < end and (new_board_end.board == game_board_end.board).any():
#             print(True)
#             return car_moves, new_solution
#         else:
#             print(f'\nFalse')
            
#             return current_moves_slice, current_slice
        

#     def get_available_cars(self, cars_dict, board):
#         available_cars = {}

#         for car_id, car in cars_dict.items():
#             moveable_list = self.is_moveable(car, board)
#             if True in moveable_list:
#                 available_cars[car_id] = car
#         return available_cars


#     def get_new_pos(self, car_tup, direction, orientation):
#         '''recieves a tuple for location and a direction and moves the tuple one place'''
#         row, col = car_tup

#         if orientation == 'H':
#             if direction == 'pos':
#                 col +=1
#             elif direction == 'neg':
#                 col -= 1
#         elif orientation == 'V':
#             if direction == 'pos':
#                 row +=1
#             elif direction == 'neg':
#                 row -= 1

#         return row, col
        

#     def is_moveable(self, car, check_board):

#         position = car['position']
#         orientation = car['orientation']
#         positions_to_check = []
#         checklist = []

#         neg_pos = self.get_new_pos(position[0], 'neg', orientation)
#         positions_to_check.append(neg_pos)

#         pos_pos = self.get_new_pos(position[-1], 'pos', orientation)
#         positions_to_check.append(pos_pos)

#         for row, col in positions_to_check:
#             position = row, col
#             if row > self.size -1 or row <0 or col > self.size -1 or col <0:
#                 checklist.append(False)
#             elif check_board.board[position] == 0:
#                 checklist.append(True)
#             else:
#                 checklist.append(False)
#         return checklist
    
#     def get_random_car(self, cars_dict):
#         """Choose a random car from cars"""
        
#         key = random.choice(list(cars_dict.keys()))
        
#         return key, cars_dict[key]

#     def random_step_hc(self, new_cars_dict, board): #dictionary and board instance
#             """Does a random step for a random moveable vehicle and returns the updated board."""

#             # Get dictionary with available cars (i.e. moveable)
#             pick = self.get_available_cars(new_cars_dict, board)
            
#             # Get a random car and get moveable directions
#             car_id, car = self.get_random_car(pick)
#             # self.car = car
#             # self.car_id = car_id
            
#             moveable_list = self.is_moveable(car, board)
#             print(car, moveable_list)

#             # Pick a random direction (backwards (0) or forwards(1)) and move the car
#             direction = random.randint(0,1)
#             new_position = []
#             # If backwards, move car left or up, else right or down, 
#             if direction == 0: 
#                 if moveable_list[0] == True:
#                     for car_tup in car['position']:
#                         new_pos = self.get_new_pos(car_tup, 'neg', car['orientation'])
#                         new_position.append(new_pos)
#                     car['position'] = new_position
#                     # if hill_climb:   
#                     car_move = (car_id, '-1')
#                     new_board = brd.Board(new_cars_dict, self.size)
#                 else:
#                     for car_tup in car['position']:
#                         new_pos = self.get_new_pos(car_tup, 'pos', car['orientation'])
#                         new_position.append(new_pos)
#                     car['position'] = new_position
#                     # if hill_climb:
#                     car_move = (car_id, '1')
#                     new_board = brd.Board(new_cars_dict, self.size)
                    
#             # Elif forwards, move car right or down, else left or up
#             elif direction == 1:
#                 if moveable_list[1] == True:
#                     for car_tup in car['position']:
#                         new_pos = self.get_new_pos(car_tup, 'pos', car['orientation'])
#                         new_position.append(new_pos)
#                     car['position'] = new_position
#                     car_move = (car_id, '1')
#                     new_board = brd.Board(new_cars_dict, self.size)
#                 else:
#                     for car_tup in car['position']:
#                         new_pos = self.get_new_pos(car_tup, 'neg', car['orientation'])
#                         new_position.append(new_pos)
#                     car['position'] = new_position
#                     car_move = (car_id, '-1')
#                     new_board = brd.Board(new_cars_dict, self.size)
            

#             print("car after move", car)
#             return new_board, car_move, new_cars_dict
            

if __name__ == '__main__':
    filepath = 'data/Rushhour6x6_1_test_red_only.csv'
    hc = hill_climber(filepath, [(2, 4), (2, 5)], 6)
    car_moves = hc.run_hc()
    print("solution:", car_moves)
    export_hillclimber_to_csv('results/test_hillclimb.csv', car_moves)
    animate('data/Rushhour6x6_1_test_red_only.csv', 'results/test_hillclimb.csv', 6)
    
   
