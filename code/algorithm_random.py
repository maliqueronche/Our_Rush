import board
import classes
import random

class Random_algorithm():
    
    def __init__(self, cars_dict, game_board):
        self.cars = cars_dict
        self.board = game_board

    def random_step(self): #dictionary and board instance
        moveable = False

        while moveable == False:
            car_id, car = self.get_random_car()
            self.car = car
            self.car_id = car_id
            moveable_list = self.is_moveable()
            if True in moveable_list:
                moveable = True
        side = random.randint(0,1)
        if side == 0: 
            if moveable_list[0] == True:
                if self.orientation == 'H':
                    self.board.move_car(self.car_id, 'left')
                else :
                    self.board.move_car(self.car_id, 'up')
            else:
                if self.orientation == 'H':
                    self.board.move_car(self.car_id, 'right')
                else:
                    self.board.move_car(self.car_id, 'down')
        if side == 1:
            if moveable_list[1] == True:
                if self.orientation == 'H':
                    self.board.move_car(self.car_id, 'right')
                else:
                    self.board.move_car(self.car_id, 'down')
            else:
                if self.orientation == 'H':
                    self.board.move_car(self.car_id, 'left')
                else :
                    self.board.move_car(self.car_id, 'up')
        return self.board


    def get_random_car(self):
        key = random.choice(list(self.cars.keys()))
        return key, self.cars[key]

    def is_moveable(self):
        positions_list = self.car.position
        orientation = self.car.orientation
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
