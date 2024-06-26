
import queue
import copy
import numpy as np
#from algorithm_random import get_available_cars, is_moveable
#from board import move_car
import board
#from classes import change_position
import copy
from pprint import pprint
import time

class depth_first_algorithm():
    """Contains functions to run the breadth first algorithm"""


    def __init__(self, size):
        print ('initializing...')
        self.size = size


    def search_depth(self, car_ins_dict, bb=False):
        """Search algorithm that searches a complete layer for a solution, before moving on to the next layer."""
        
            
        # Create copy of instances of cars with only relevant data
        cars_dict = {}
        for car_id, car in car_ins_dict.items():
            position_car = car.position
            orientation_car = car.orientation
            cars_dict[car_id] = {'id' : car_id, 'position' : position_car, 'orientation': orientation_car}
        
        if self.size == 6:
            end_position = [(2,4), (2, 5)]
            depth_limit = 1000
        elif self.size == 9:
            end_position = [(4, 7), (4, 8)]
            depth_limit = 5000
        elif self.size == 12:
            end_position = [(5, 10), (5, 11)]
            depth_limit = 10000


        # Create queue, starting board and archive to check for duplicate boards
        df_stack = [("", 0)]
        starting_board = board.Board(cars_dict, self.size)
        starting_board = tuple(map(tuple, starting_board.board))
        # archive = {starting_board}

        # dictionary containing all states
        state_dict = {}
        state_dict[""] = cars_dict
        
        # Solution by default not found 
        solution_found = False
        

        j = 0
        # start = time()
        t_end = time.time() + 15
        

        while time.time() < t_end:

            df_stack = [("", 0)]
            print("new_round")
            state_dict = {}
            state_dict[""] = cars_dict
            if time.time() % 30 == 0:
                print("time_remaining:", round(t_end - time.time(), 2), "seconds")
            archive = {starting_board}
            print(depth_limit)

            while len(df_stack) > 0:
                # print(len(df_stack))
            # for i in range(12):
                j += 1

                # Print duration over iteration length
                # if j % 10000 == 0:
                #     end = time()
                #     print('\niteration:', j)
                #     print(f'The time elapsed: {end-start:.2f} seconds.')
                #     start = time()
                
                # Get state from queue
                state, depth = df_stack.pop()
                
                if bb and depth >= depth_limit:
                    
                    continue
                # Get dictionary current cars (id: pos(tup), or(str), par(set))
                current_cars_dict = state_dict[state]
                
                # Create current board (Numpy arrays)
                current_board = board.Board(current_cars_dict, self.size)
                
                # Get a dict of available cars (id: pos(tup), or(str), par(set))
                available_cars = self.get_available_cars(current_cars_dict, current_board.board) # shorter dictionary with available vehicles
            
                # Loop over available cars, move them, add new states to queue
                for car_id, car in available_cars.items():
                    if car_id == 88 and car['position'] == end_position:
                        if bb:
                            best_solution = state
                            
                            break
                        else: 
                            return state

                    # Copy current dictionary
                    new_cars_dict = copy.deepcopy(current_cars_dict)
                    
                    # Get's a tuple for every side if it is moveable
                    moveable = self.is_moveable(car, current_board.board)
                    
                    # Move car backwards if possible
                    if moveable[0]:

                        # Changes the position of a car
                        new_position = []
                        car = new_cars_dict[car_id]
                        for car_tup in car['position']:
                            new_pos = self.get_new_pos(car_tup, 'neg', car['orientation'])
                            new_position.append(new_pos)
                        car['position']= new_position

                        # Create new statename
                        new_state = (state + str(car_id) + ',' + '-' + ',')
                        
                        # Check if the red car is on the right position
                        if car_id == 88 and car['position'] == end_position:
                            if bb:
                                best_solution = new_state
                                depth_limit = depth
                                
                                break
                            else: 
                                return new_state

                        # Create new board (Numpy arrays)
                        new_board = board.Board(new_cars_dict, self.size)
                        new_board = tuple(map(tuple, new_board.board))     
                            
                        # Check if board is not in archive and add to queue
                        if new_board not in archive:
                            archive.add(new_board)
                            df_stack.append((new_state, depth + 1))
                            state_dict[new_state] = new_cars_dict
                    
                    new_cars_dict = copy.deepcopy(current_cars_dict)
                    
                    # Move car forwards if possible
                    if moveable[1]:
                        
                        # Changes position of car
                        new_position = []
                        car = new_cars_dict[car_id]
                        for car_tup in car['position']:
                            new_pos = self.get_new_pos(car_tup, 'pos', car['orientation'])
                            new_position.append(new_pos)
                        car['position']= new_position
                        
                        # Create new state
                        new_state = (state + str(car_id) + ',' + '+' + ',')
                        
                        # Check to see if red car is on right place
                        if car_id == 88 and car['position'] == end_position:
                            if bb:
                                best_solution = new_state
                                depth_limit = depth
                                
                                break
                            else: 
                                return new_state


                        # Create new board
                        new_board = board.Board(new_cars_dict, self.size)
                        new_board = tuple(map(tuple, new_board.board))

                        # Check if board is not in archive and add to queue
                        if new_board not in archive:
                            archive.add(new_board)
                            df_stack.append((new_state, depth + 1))
                            state_dict[new_state] = new_cars_dict
                
                # Remove old states out of the state dict
                # del state_dict[state]
            
            
                
         
            
            # print("depth_limit", depth_limit)

        return best_solution if best_solution else "No solution found within depth limit"


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
            elif board[position] == 0:
                checklist.append(True)
            else:
                checklist.append(False)
        return checklist
    
    
    