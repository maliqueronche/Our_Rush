
import copy
import numpy as np
import board
from pprint import pprint
from time import time

class iterative_deepening_algorithm():
    """
    Contains functions to run the iterative deepening depth-first search algorithm.
    """

    def __init__(self, size):
        """
        Initializes the algorithm with the board size.
        """

        print ('initializing...')
        self.size = size

    def search_depth_iteratively(self, car_ins_dict):
        """
        Performs iterative deepening search to find a solution, increasing depth limits progressively.
        """
        # create copy of instances of cars with only relevant data
        cars_dict = {car_id: {'id': car_id, 'position': car.position, 'orientation': car.orientation} 
                     for car_id, car in car_ins_dict.items()}

        # set end position and initial depth limit based on board size
        if self.size == 6:
            end_position = [(2,4), (2, 5)]
            depth_limit = 0
        elif self.size == 9:
            end_position = [(4, 7), (4, 8)]
            depth_limit = 500
        elif self.size == 12:
            end_position = [(5, 10), (5, 11)]
            depth_limit = 1000

        # initialize stack, starting board, and archive to check for duplicate boards
        df_stack = [("", 0)]
        starting_board = board.Board(cars_dict, self.size)
        starting_board = tuple(map(tuple, starting_board.board))
        archive = {starting_board}

        # dictionary containing all states
        state_dict = {"": cars_dict}
        
        # solution by default not found 
        solution_found = False
        
        j = 0
        start = time()

        while not solution_found:
            depth_limit += 1
            df_stack = [("", 0)]
            archive = {starting_board}
            state_dict = {"": cars_dict}
            

            while df_stack:
                j += 1

                # print duration over iteration length
                if j % 10000 == 0:
                    end = time()
                    print('\niteration:', j)
                    print(f'The time elapsed: {end-start:.2f} seconds.')
                    start = time()
                
                # get state from stack
                state, depth = df_stack.pop()
                if depth > depth_limit:
                    continue
                
                # get dictionary current cars 
                current_cars_dict = state_dict[state]
                
                # create current board
                current_board = board.Board(current_cars_dict, self.size)
                
                # get a dict of available cars
                available_cars = self.get_available_cars(current_cars_dict, current_board.board) # shorter dictionary with available vehicles
            
                # loop over available cars, move them, add new states to stack
                for car_id, car in available_cars.items():
                    if car_id == 88 and car['position'] == end_position:
                        return state

                    new_cars_dict = copy.deepcopy(current_cars_dict)
                    moveable = self.is_moveable(car, current_board.board)
                    if moveable[0]:
                        self.move_car(new_cars_dict[car_id], 'neg')
                        new_state = state + f"{car_id},-,"
                        if car_id == 88 and new_cars_dict[car_id]['position'] == end_position:
                            return new_state
                        self.add_state_to_stack(new_cars_dict, new_state, archive, df_stack, state_dict, depth)

                    # move car forwards if possible
                    new_cars_dict = copy.deepcopy(current_cars_dict)
                    if moveable[1]:
                        self.move_car(new_cars_dict[car_id], 'pos')
                        new_state = state + f"{car_id},+,"
                        if car_id == 88 and new_cars_dict[car_id]['position'] == end_position:
                            return new_state
                        self.add_state_to_stack(new_cars_dict, new_state, archive, df_stack, state_dict, depth)

                del state_dict[state]

        return "No solution found within depth limit"


    def get_available_cars(self, cars_dict, board):
        """
        Returns a dictionary of moveable cars based on the current board state.
        """
        available_cars = {}


        for car_id, car in cars_dict.items():
            moveable_list = self.is_moveable(car, board)
            if True in moveable_list:
                available_cars[car_id] = car
        return available_cars

    def get_new_pos(self, car_tup, direction, orientation):
        '''
        Recieves a tuple for location and a direction and moves the tuple one place
        '''
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
        positions_to_check = [
            self.get_new_pos(position[0], 'neg', orientation),
            self.get_new_pos(position[-1], 'pos', orientation)
        ]

        checklist = []
        for row, col in positions_to_check:
            if row < 0 or row >= self.size or col < 0 or col >= self.size:
                checklist.append(False)
            else:
                checklist.append(board[row, col] == 0)
        return checklist

    def move_car(self, car, direction):
        """
        Moves a car in the specified direction.
        """
        new_position = [self.get_new_pos(pos, direction, car['orientation']) for pos in car['position']]
        car['position'] = new_position

    def add_state_to_stack(self, new_cars_dict, new_state, archive, df_stack, state_dict, depth):
        """
        Adds a new state to the stack if it hasn't been seen before.
        """
        new_board = board.Board(new_cars_dict, self.size)
        new_board_tuple = tuple(map(tuple, new_board.board))
        if new_board_tuple not in archive:
            archive.add(new_board_tuple)
            df_stack.append((new_state, depth + 1))
            state_dict[new_state] = new_cars_dict