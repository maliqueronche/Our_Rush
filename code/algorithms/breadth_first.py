
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

    def search_breadth(self):

        end_position = self.cars[88].position

        queue = queue.Queue()
        queue.put(game_board)

        while self.cars[ord('X')].position != [(2,4), (2,5)]:

            state = queue.get()

            available_cars = get_available_cars(self.cars)
            
            
            for car in available_cars:

                moveable_list = is_moveable(car)
                
                # Make all possible moves for car:
                
                if moveable_list[0] == True:
                    if car.orientation == 'H':
                        new_state = copy.deepcopy(state)
                        new_state.move_car(car.ID, 'left')
                        queue.put(new_state)
                        car.change_position('left')
                    else :
                        self.board.move_car(self.car_id, 'up')
                        self.car.change_position('up')
                else:
                    if self.orientation == 'H':
                        self.board.move_car(self.car_id, 'right')
                        self.car.change_position('right')
                    else:
                        self.board.move_car(self.car_id, 'down')
                        self.car.change_position('down')



                    # Move car --> new state 
                    # if new_state not in archive:
                        # add new state to queue
                        # update car_position in self.cars
                        # dictionary containing paths (keys) and lists of moves (values) which are tuples (car, move)
                



def main():
    

if __name__ == '__main__':
    main()

