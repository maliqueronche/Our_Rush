
import queue
import copy
from algorithm_random import get_available_cars, is_moveable
from board import move_car
from classes import change_position
import copy

class breadth_first_algorithm():
    """Contains functions to run the breadth first algorithm"""


    def __init__(self, cars_dict, game_board):

        self.cars = cars_dict
        self.board = game_board

    def search_breadth(self, cars_dict):

        end_position = self.cars[88].position

        queue = queue.Queue()
        
        archive = set()

        state_dict = {}
        state_dict["start"] = cars_dict
    
        queue.put("start")
        solution_found = False

        

        while not solution_found:

            state = queue.get()
            current_cars_dict = state_dict[state]
            
            available_cars = get_available_cars(current_cars_dict)
            
            
            for car in available_cars:

                moveable_list = is_moveable(car)
                
                # Make all possible moves for car:
                # TODO: kan niet zomaar cars dictionary updaten, want ik wil meerdere states kunnen opslaan.
                
                if moveable_list[0] == True:
                    if car.orientation == 'H':
                        new_board.move_car(car.ID, 'neg', car.orientation)
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
    

    def get_available_cars(self, cars_dict):

        board = np.zeros((size, size))

        for id, vehicle in cars_dict.items():
            location = vehicle.position
            for tup in location:
                board[tup] = vehicle.ID


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

        positions_list = car.position
        orientation = car.orientation
        positions_to_check = []
        checklist = []

        neg_pos = board.get_new_pos(positions_list[0], 'neg', 'orientation')
        positions_to_check.append(neg_pos)
        pos_pos = board.get_new_pos(positions_list[-1], 'pos', 'orientation')
        positions_to_check.append(pos_pos)

        for row, col in positions_to_check:
                position = row, col
                if row > board.size -1 or row <0 or col > board.size -1 or col <0:
                    checklist.append(False)
                elif board[position] == 0:
                    checklist.append(True)
                else:
                    checklist.append(False)
        return checklist






def main():
    

if __name__ == '__main__':
    main()

