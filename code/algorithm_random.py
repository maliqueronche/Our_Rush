import board
import classes
import random
# import visualization
import copy

class Random_algorithm():
    """
    Contains functions to execute random algorithm.
    - init: initialises cars and board in this class.
    - random_step: does a random step for a random moveable vehicle.
    - get_random_car: gets a random car.
    - get_available_cars: gets all cars that can move.
    - is_moveable: checks if car is moveable.
    """
    
    def __init__(self, cars_dict, game_board):
        """
        Initialise cars and board
        """

        self.cars = cars_dict
        self.board = game_board

    def random_step(self, hill_climb = False): #dictionary and board instance
        """
        Does a random step for a random moveable vehicle and returns the updated board.
        """

        # set moveable by default to False
        moveable = False

        # get dictionary with available cars (i.e. moveable)
        pick = self.get_available_cars(self.cars)
        
        # get a random car and get moveable directions
        car_id, car = self.get_random_car(pick)
        self.car = car
        self.car_id = car_id
        orientation = self.car.orientation
        moveable_list = self.is_moveable(car)
        
        # pick a random direction (backwards (0) or forwards(1)) and move the car
        direction = random.randint(0,1)

        # if backwards, move car left or up, else right or down 
        if direction == 0: 
            if moveable_list[0] == True:
                self.board.move_car(self.car_id, 'neg')  
                car_move = (car_id, '-1')
                board = self.board
                self.car.change_position('neg', orientation)
            else:
                self.board.move_car(self.car_id, 'pos')
                car_move = (car_id, '1')
                board = self.board
                self.car.change_position('pos', orientation)
                
        # elif forwards, move car right or down, else left or up
        elif direction == 1:
            if moveable_list[1] == True:
                self.board.move_car(self.car_id, 'pos')
                car_move = (car_id, '1')
                board = self.board
                self.car.change_position('pos', orientation)
               
            else:
                self.board.move_car(self.car_id, 'neg')
                car_move = (car_id, '-1')
                board = self.board
                self.car.change_position('neg', orientation)
        
        self.cars[car_id] = car
        updated_cars_dict = self.cars

        
        return car_move

    def get_random_car(self, cars_dict):
        """
        Choose a random car from cars
        """
        
        key = random.choice(list(cars_dict.keys()))
        
        return key, cars_dict[key]
    
    def get_available_cars(self, car_dict):
        """"
        For every car in cars, if it is moveable, add the car to available cars and return that dictionary.
        """

        available_cars = {}

        # loop over cars, check if a car can move and add it to dictionary
        for car in self.cars.keys():
            
            moveable_list = self.is_moveable(self.cars[car])
            
            if True in moveable_list:
                available_cars[car] = self.cars[car]
                
        return available_cars

    def is_moveable(self, car):
        """
        Takes a car, checks if it can move and returns list with tuples containing True or False.
        """

        positions_list = car.position
        orientation = car.orientation
        self.orientation = orientation
        positions_to_check = []
        checklist = []

        # get positions to check 
        neg_pos = self.board.get_new_pos(positions_list[0], 'neg', orientation)
        positions_to_check.append(neg_pos)
        pos_pos = self.board.get_new_pos(positions_list[-1], 'pos', orientation)
        positions_to_check.append(pos_pos)
        
        # check if position can be moved to
        for row, col in positions_to_check:
                position = row, col
                if row > self.board.size -1 or row <0 or col > self.board.size -1 or col <0:
                    checklist.append(False)
                elif self.board.board[position] == 0:
                    checklist.append(True)
                else:
                    checklist.append(False)
        return checklist
