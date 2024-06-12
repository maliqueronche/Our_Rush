import board
import classes
import random

class Random_algorithm():
    
    def __init__(self, cars_dict, game_board):
        self.cars = cars_dict
        self.board = game_board

    def random_step(self): #dictionary and board instance
        moveable = False
        pick = self.get_available_cars()

        while moveable == False:
            car_id, car = self.get_random_car(pick)
            self.car = car
            self.car_id = car_id
            moveable_list = self.is_moveable(car)
            if True in moveable_list:
                moveable = True

        side = random.randint(0,1)

        if side == 0: 
            if moveable_list[0] == True:
                if self.orientation == 'H':
                    self.board.move_car(self.car_id, 'left')
                    self.car.change_position('left')
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
        elif side == 1:
            if moveable_list[1] == True:
                if self.orientation == 'H':
                    self.board.move_car(self.car_id, 'right')
                    self.car.change_position('right')
                else:
                    self.board.move_car(self.car_id, 'down')
                    self.car.change_position('down')
            else:
                if self.orientation == 'H':
                    self.board.move_car(self.car_id, 'left')
                    self.car.change_position('left')
                else :
                    self.board.move_car(self.car_id, 'up')
                    self.car.change_position('up')

        return self.board


    def get_random_car(self, cars_dict):
        key = random.choice(list(cars_dict.keys()))
        return key, cars_dict[key]
    
    def get_available_cars(self):
        available_cars = {}
        for car in self.cars.keys():
            moveable_list = self.is_moveable(self.cars[car])
            if True in moveable_list:
                available_cars[car] = self.cars[car]
        return available_cars

    def is_moveable(self, car):
        positions_list = car.position
        orientation = car.orientation
        self.orientation = orientation
        positions_to_check = []
        checklist = []

        if orientation == 'H':
            left_pos = self.board.get_new_pos(positions_list[0], 'left')
            positions_to_check.append(left_pos)
            right_pos = self.board.get_new_pos(positions_list[-1], 'right')
            positions_to_check.append(right_pos)
        if orientation == 'V':
            up_pos = self.board.get_new_pos(positions_list[0], 'up')
            positions_to_check.append(up_pos)
            down_pos = self.board.get_new_pos(positions_list[-1], 'down')
            positions_to_check.append(down_pos)
        
        for row, col in positions_to_check:
                position = row, col
                if row > self.board.size -1 or row <0 or col > self.board.size -1 or col <0:
                    checklist.append(False)
                elif self.board.board[position] == 0:
                    checklist.append(True)
                else:
                    checklist.append(False)
        return checklist
