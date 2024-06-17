
import queue
import copy
import numpy
#from algorithm_random import get_available_cars, is_moveable
#from board import move_car
import board
#from classes import change_position
import copy

class breadth_first_algorithm():
    """Contains functions to run the breadth first algorithm"""


    def __init__(self, size):
        print ('initializing')
        self.size = size


    def search_breadth(self, car_ins_dict):

        cars_dict = {}
        for car_id, car in car_ins_dict.items():
            position_car = car.position
            orientation_car = car.orientation
            cars_dict[car_id] = {'id' : car_id, 'position' : position_car, 'orientation': orientation_car}
        print (cars_dict)

        end_position = [(2,4), (2,5)]

        bf_queue = queue.Queue()
        starting_board = board.Board(cars_dict, self.size)
        archive = {starting_board}

        state_dict = {}
        state_dict["start"] = cars_dict
    
        bf_queue.put("start")
        solution_found = False

        # while not solution_found:
        for i in range(3):

            state = bf_queue.get()  # This is a sequence of steps
            current_cars_dict = state_dict[state] # this is the dictionary with the vehicles
            
            current_board = board.Board(current_cars_dict, self.size)
            print (current_board.board)
            available_cars = self.get_available_cars(current_cars_dict, current_board.board) # shorter dictionary with available vehicles
            print (available_cars)
            
            
            for car_id, car in available_cars.items():

                moveable = self.is_moveable(car, current_board.board)  #[True, False]
                
                # Make all possible moves for car:
                # TODO: kan niet zomaar cars dictionary updaten, want ik wil meerdere states kunnen opslaan.
                
                if moveable[0] == True:
                    print (car)
                    new_position = []
                    for car_tup in car['position']:
                        new_pos = self.get_new_pos(car_tup, 'neg', car['orientation'])
                        new_position.append(new_pos)
                    car['position']= new_position
                    print (car)
                    if new_board not in archive:
                        archive.add(new_state)
                        queue.put()
                        state_dict[sequence] = posdict
                        car.change_position('neg')
  
                   # Move car --> new state 
                    # if new_state not in archive:
                        # add new state to queue
                        # update car_position in self.cars
                        # dictionary containing paths (keys) and lists of moves (values) which are tuples (car, move)
    

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
        print (board)

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



    
if __name__ == '__main__':
    breadth_first_algorithm.search_breadth

