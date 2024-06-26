
import queue
import copy
import numpy as np
import board
import copy
from pprint import pprint
import time

class depth_first_algorithm():
    """
    Executes the depth-first search (DFS) algorithm with optional heuristic controls.
    """
    def __init__(self, size):
        """
        Initializes the algorithm with a specified board size.
        """
        print('initializing...')
        self.size = size

    def search_depth(self, car_ins_dict, bb=False):
        """
        Iteratively searches with increasing depth limits to find the optimal solution. 
        Uses heuristic if enabled.
        """

        # create copy of instances of cars with only relevant data
        cars_dict = {}
        for car_id, car in car_ins_dict.items():
            position_car = car.position
            orientation_car = car.orientation
            cars_dict[car_id] = {'id': car_id, 'position': position_car, 'orientation': orientation_car}
        
        # set the end position and initial depth limit based on the board size
        if self.size == 6:
            end_position = [(2, 4), (2, 5)]
            initial_depth_limit = 1000
        elif self.size == 9:
            end_position = [(4, 7), (4, 8)]
            initial_depth_limit = 5000
        elif self.size == 12:
            end_position = [(5, 10), (5, 11)]
            initial_depth_limit = 10000

        # initialize the starting board and data structures for the search
        starting_board = board.Board(cars_dict, self.size)
        starting_board_tuple = tuple(map(tuple, starting_board.board))
        archive = {starting_board}
        state_dict = {"": cars_dict}

        # solution by default not found 
        best_solution = None
        best_solution_depth = initial_depth_limit
        
        # set the time limit for the search
        t_end = time.time() + 5

         # begin iterative deepening search
        while time.time() < t_end:
            df_stack = [("", 0)]
            state_dict = {"": cars_dict}
            archive = {starting_board_tuple}

            while len(df_stack) > 0:
                state, depth = df_stack.pop()
                
                if depth >= best_solution_depth:
                    continue

                current_cars_dict = state_dict[state]
                current_board = board.Board(current_cars_dict, self.size)
                available_cars = self.get_available_cars(current_cars_dict, current_board.board)

                for car_id, car in available_cars.items():
                    if car_id == 88 and car['position'] == end_position:
                        best_solution = state + str(car_id) + ',' + '+' + ','
                        best_solution_depth = depth
                        break

                    new_cars_dict = copy.deepcopy(current_cars_dict)
                    moveable = self.is_moveable(car, current_board.board)
                    
                    if moveable[0]:
                        new_position = []
                        car = new_cars_dict[car_id]
                        for car_tup in car['position']:
                            new_pos = self.get_new_pos(car_tup, 'neg', car['orientation'])
                            new_position.append(new_pos)
                        car['position'] = new_position

                        new_state = state + str(car_id) + ',' + '-' + ','
                        if car_id == 88 and car['position'] == end_position:
                            best_solution = new_state
                            best_solution_depth = depth
                            break
                        
                        new_board = board.Board(new_cars_dict, self.size)
                        new_board_tuple = tuple(map(tuple, new_board.board))
                        if new_board_tuple not in archive:
                            archive.add(new_board_tuple)
                            df_stack.append((new_state, depth + 1))
                            state_dict[new_state] = new_cars_dict
                    
                    new_cars_dict = copy.deepcopy(current_cars_dict)
                    
                    if moveable[1]:
                        new_position = []
                        car = new_cars_dict[car_id]
                        for car_tup in car['position']:
                            new_pos = self.get_new_pos(car_tup, 'pos', car['orientation'])
                            new_position.append(new_pos)
                        car['position'] = new_position
                        
                        new_state = state + str(car_id) + ',' + '+' + ','
                        if car_id == 88 and car['position'] == end_position:
                            best_solution = new_state
                            best_solution_depth = depth
                            break

                        new_board = board.Board(new_cars_dict, self.size)
                        new_board_tuple = tuple(map(tuple, new_board.board))
                        if new_board_tuple not in archive:
                            archive.add(new_board_tuple)
                            df_stack.append((new_state, depth + 1))
                            state_dict[new_state] = new_cars_dict

                if best_solution_depth == depth:
                    break
            
            if best_solution_depth == depth:
                best_solution_depth -= 1  # Decrease depth limit for next iteration
                print("New depth limit:", best_solution_depth)
                if best_solution_depth < 0:
                    break  # Ensure depth limit does not go negative

        return best_solution if best_solution else "No solution found within depth limit"





    def get_available_cars(self, cars_dict, board):
        """
        Returns a dictionary of cars that are moveable based on the current board state.
        """
        available_cars = {}

        for car_id, car in cars_dict.items():
            moveable_list = self.is_moveable(car, board)
            if True in moveable_list:
                available_cars[car_id] = car
        return available_cars


    def get_new_pos(self, car_tup, direction, orientation):
        """
        Recieves a tuple for location and a direction and moves the tuple one place
        """
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
        """
        Determines if the car is moveable in its current orientation within the board constraints.
        """

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
            elif board[position] == 0:
                checklist.append(True)
            else:
                checklist.append(False)
        return checklist
    
    
    