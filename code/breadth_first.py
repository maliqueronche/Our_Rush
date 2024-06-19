
import queue
import copy
import numpy as np
#from algorithm_random import get_available_cars, is_moveable
#from board import move_car
import board
#from classes import change_position
import copy
from pprint import pprint
from time import time

class breadth_first_algorithm():
    """Contains functions to run the breadth first algorithm"""


    def __init__(self, size):
        print ('initializing')
        self.size = size


    def search_breadth(self, car_ins_dict):
        """Search algorithm that searches a complete layer for a solution, before moving on to the next layer."""

        # Create copy of instances of cars with only relevant data
        cars_dict = {}
        for car_id, car in car_ins_dict.items():
            position_car = car.position
            orientation_car = car.orientation
            cars_dict[car_id] = {'id' : car_id, 'position' : position_car, 'orientation': orientation_car,'parents' : {}}
        

        end_position = [(2,4), (2, 5)]

        # Create queue, starting board and archive to check for duplicate boards
        bf_queue = queue.Queue()
        starting_board = board.Board(cars_dict, self.size)
        print(starting_board.board)
        starting_board_name = tuple(map(tuple, starting_board.board))
        new_archive = {starting_board_name}

        # dictionary containing all states
        state_dict = {}
        state_dict[""] = cars_dict
    
        # Add start state to queue 
        bf_queue.put("")
        
        # Solution by default not found 
        solution_found = False

        j = 0
        start = time()
        while not solution_found:
        # for i in range(1):
            j += 1
            
            state = bf_queue.get()
            
            # Get dictionary current cars (id: pos(tup), or(str), par(set))
            current_cars_dict = state_dict[state] 

            # Create current board (Numpy arrays)
            current_board = board.Board(current_cars_dict, self.size)
            
            # Get a dict of available cars (id: pos(tup), or(str), par(set))
            available_cars = self.get_available_cars(current_cars_dict, current_board.board) # shorter dictionary with available vehicles


            if j % 10000 == 0:
                end = time()
                
                print('\niteration:', j)
                print("a state at this point:", state)
                print("board", current_board.board)
                print("available cars", available_cars)
                print(f'The time elapsed: {end-start:.2f} seconds.')
                
                start = time()
            
            # Loop over available cars, move them, add new states to queue
            for car_id, car in available_cars.items():

                # Copy current dictionary
                new_cars_dict = copy.deepcopy(current_cars_dict)

                # Get's a tuple for every side if it is moveable
                moveable = self.is_moveable(car, current_board.board)
                
                # Copies the state of the parent
                current_state = state

                # Move car backwards if possible
                while moveable[0] == True:

                    # Changes the position of a car
                    new_position = []
                    car = new_cars_dict[car_id]
                    for car_tup in car['position']:
                        new_pos = self.get_new_pos(car_tup, 'neg', car['orientation'])
                        new_position.append(new_pos)
                    car['position']= new_position

                    # Create new statename
                    new_state = (current_state + str(car_id) + '-' + ' ')

                    # Check if the red car is on the right position
                    if car_id == 88 and car['position'] == end_position:
                        solution_found = True
                        return new_state    

                    # Create new board (Numpy arrays)
                    new_board = board.Board(new_cars_dict, self.size)
                    # Create new boardName
                    new_board_name = tuple(map(tuple, new_board.board))     
                           
                    # Check if the board is in the parent string and add to queue
                    if new_board_name not in car['parent']:
                        new_archive.add(new_board)
                        new_cars_dict['parent'].add(new_board_name)
                        bf_queue.put(new_state)
                        state_dict[new_state] = new_cars_dict

                    moveable = self.is_moveable(car, new_board)
                    current_state = new_state
                    
                    # if moveable[0] == True: #????
                    #     new_cars_dict = copy.deepcopy(new_cars_dict)
                    #     # new_archive = copy.deepcopy(new_archive)

                moveable = self.is_moveable(car, current_board.board)
                current_state = state
                        
                while moveable[1] == True:
                    
                    # Changes position of car
                    new_position = []
                    for car_tup in car['position']:
                        new_pos = self.get_new_pos(car_tup, 'pos', car['orientation'])
                        new_position.append(new_pos)
                    car['position']= new_position
                    
                    # Create new state
                    new_state = (current_state + str(car_id) + '+' + ' ')

                    # Check to see if red car is on right place
                    if car_id == 88 and car['position'] == end_position:
                        solution_found = True
                        return new_state 

                    # Create new board
                    new_board = board.Board(new_cars_dict, self.size)
                    new_board_name = tuple(map(tuple, new_board.board))

                    if new_board_name not in car['parent']:
                        car['parent'].add(new_board_name)
                        new_archive.add(new_board)
                        bf_queue.put(new_state)
                        state_dict[new_state] = new_cars_dict

                    new_board = np.array(new_board_name)
                    moveable = self.is_moveable(car, new_board)
                    current_state = new_state

            # Remove old states out of the state dict
            del state_dict[state]
            
        return new_state

                        
    

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
        # print (board)

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
    
    def check_moves(moveable, place):
        if place == 0:
            side = 'neg'
            min_plus = '-'
        elif place == 1:
            side = 'pos'
            min_plus = '+'

        while moveable[place] == True: #while moveable[0]
            new_position = []
            car = new_cars_dict[car_id]
            for car_tup in car['position']:
                new_pos = self.get_new_pos(car_tup, side, car['orientation'])
                new_position.append(new_pos)
            car['position']= new_position

            # Create new state
            new_state = (current_state + str(car_id) + min_plus + ' ')

            # Create new board
            new_board = board.Board(new_cars_dict, self.size)

            if car_id == 88 and car['position'] == end_position:
                solution_found = True
                return new_state            
            
            new_board = tuple(map(tuple, new_board.board))
                    
            if new_board not in new_archive:
                new_archive.add(new_board)
                new_cars_dict['parent'].add(new_board)
                bf_queue.put(new_state)
                if new_state not in state_dict.keys():
                    state_dict[new_state] = new_cars_dict

            new_board = np.array(new_board)
            moveable = self.is_moveable(car, new_board)
            current_state = new_state

            if moveable[0] == True:
                new_cars_dict = copy.deepcopy(new_cars_dict)
                # new_archive = copy.deepcopy(new_archive)




    
if __name__ == '__main__':
    breadth_first_algorithm.search_breadth

