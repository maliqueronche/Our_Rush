# Algorithm based on 'logic'

class Logic():
    def __init__(self, cars_dict, game_board):
        self.cars = cars_dict
        self.game_board = game_board

    def solve_board(self):
        while self.cars[ord('X')].position != [(2,4), (2,5)]:
            move_red_car()


    def move_red_car(self):
        red_car = self.cars[ord('X')]
        moveable = is_moveable(red_car)
        if moveable == True:
            self.game_board.move_car(ord('X'), 'pos', 'H')
        else :
            get_step_sequence():

    def is_moveable(self, car):



    def get_step_sequence(self):
