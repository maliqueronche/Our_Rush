
import queue
import copy
import numpy as np
import board
import copy
from pprint import pprint
from time import time

class breadth_first_algorithm():

    """
    Contains functions to run the breadth first algorithm
    """
    
    def __init__(self, size):
        """
        Initializes the algorithm with a specified board size.
        """

        print ('initializing...')
        self.size = size


    def search_breadth(self, car_ins_dict):
        """
        Executes the breadth-first search algorithm to find a solution.
        Returns: str: The best solution found within the depth limit, or a message indicating no solution was found.
        """

        # create copy of instances of cars with only relevant data
        cars_dict = {}
        for car_id, car in car_ins_dict.items():
            position_car = car.position
            orientation_car = car.orientation
            cars_dict[car_id] = {'id' : car_id, 'position' : position_car, 'orientation': orientation_car}
        
        # set end position based on board size
        if self.size == 6:
            end_position = [(2,4), (2, 5)]
        elif self.size == 9:
            end_position = [(4, 7), (4, 8)]
        elif self.size == 12:
            end_position = [(5, 10), (5, 11)]

        # create queue, starting board and archive to check for duplicate boards
        bf_queue = queue.Queue()
        starting_board = board.Board(cars_dict, self.size)
        starting_board = tuple(map(tuple, starting_board.board))
        archive = {starting_board}

        # dictionary containing all states
        state_dict = {"": cars_dict}
    
        # Add start state to queue 
        bf_queue.put("")
        
        # Solution by default not found 
        solution_found = False

        j = 0
        start = time()
        while not solution_found:
            j += 1

            # print duration over iteration length
            if j % 10000 == 0:
                end = time()
                print('\niteration:', j)
                print("a state at this iteration:", state)
                print(f'The time elapsed: {end-start:.2f} seconds.')
                start = time()
            
            # get state from queue
            state = bf_queue.get()
            
            # get dictionary current cars (id: pos(tup), or(str), par(set))
            current_cars_dict = state_dict[state] 
            
            # create current board (Numpy arrays)
            current_board = board.Board(current_cars_dict, self.size)
            
            # get dict of available cars (id: pos(tup), or(str), par(set))
            available_cars = self.get_available_cars(current_cars_dict, current_board.board) # shorter dictionary with available vehicles
        
            # loop over available cars, move them, add new states to queue
            for car_id, car in available_cars.items():

                # copy current dictionary
                new_cars_dict = copy.deepcopy(current_cars_dict)

                # get's a tuple for every side if it is moveable
                moveable = self.is_moveable(car, current_board.board)
                
                # move car backwards if possible
                if moveable[0]:

                    # changes the position of a car
                    new_position = []
                    car = new_cars_dict[car_id]
                    for car_tup in car['position']:
                        new_pos = self.get_new_pos(car_tup, 'neg', car['orientation'])
                        new_position.append(new_pos)
                    car['position']= new_position

                    # create new statename
                    new_state = (state + str(car_id) + ',' + '-' + ',')
                    
                    # check if the red car is on the right position
                    if car_id == 88 and car['position'] == end_position:
                        solution_found = True
                        return new_state    

                    # create new board (Numpy arrays)
                    new_board = board.Board(new_cars_dict, self.size)
                    new_board = tuple(map(tuple, new_board.board))     
                           
                    # check if board is not in archive and add to queue
                    if new_board not in archive:
                        archive.add(new_board)
                        bf_queue.put(new_state)
                        state_dict[new_state] = new_cars_dict
                
                new_cars_dict = copy.deepcopy(current_cars_dict)
                
                # move car forwards if possible
                if moveable[1]:
                    
                    # changes position of car
                    new_position = []
                    car = new_cars_dict[car_id]
                    for car_tup in car['position']:
                        new_pos = self.get_new_pos(car_tup, 'pos', car['orientation'])
                        new_position.append(new_pos)
                    car['position']= new_position
                    
                    # create new state
                    new_state = (state + str(car_id) + ',' + '+' + ',')
                    
                    # check to see if red car is on right place
                    if car_id == 88 and car['position'] == end_position:
                        solution_found = True
                        return new_state 

                    # create new board
                    new_board = board.Board(new_cars_dict, self.size)
                    new_board = tuple(map(tuple, new_board.board))

                    # check if board is not in archive and add to queue
                    if new_board not in archive:
                        archive.add(new_board)
                        bf_queue.put(new_state)
                        state_dict[new_state] = new_cars_dict
                
            # remove old states out of the state dict
            del state_dict[state]
        
        return best_solution if solution_found else "No solution found within depth limit"


    def get_available_cars(self, cars_dict, board):
        """
        Returns a dictionary of cars that are moveable based on the current board state.
        Returns a dictionary of available cars that can move.
        """
        available_cars = {}

        for car_id, car in cars_dict.items():
            moveable_list = self.is_moveable(car, board)
            if True in moveable_list:
                available_cars[car_id] = car
        return available_cars


    def get_new_pos(self, car_tup, direction, orientation):
        """
        recieves a tuple for location and a direction and moves the tuple one place
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
        Returns a list indicating if the car can move in negative and positive directions.
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
    

    



    
