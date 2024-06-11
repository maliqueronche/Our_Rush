import board
import classes
import random

def random_step(cars_dict, board_game): #dictionary and board instance
    car_id, car = get_random_car(cars_dict)
    moveable = is_moveable(car)

    

def get_random_car(car_dict):
    print ('get random car')
    key = random.choice(list(car_dict.keys()))
    print (key)
    return key, car_dict[key]

def is_moveable(car):
    positions_list = car.position
    orientation = car.orientation
    positions_to_check = []
    checklist = []

    if orientation == 'H':
        left_pos = board.get_new_pos(positions_list[0], 'left')
        positions_to_check.append(left_pos)
        right_pos = board.get_new_pos(positions_list[-1], 'right')
        positions_to_check.append(right_pos)
    if orientation == 'V':
        up_pos = board.get_new_pos(positions_list[0], 'up')
        positions_to_check.append(up_pos)
        down_pos = board.get_new_pos(positions_list[-1], 'right')
        positions_to_check.append(down_pos)
    
    for position in positions_to_check:
        if position.any > board.size or position.any <0:
            checklist.append(False)
        elif board.board[position] == 0:
            checklist.append(True)
        else:
            checlist.append(False)

    print (checklist)
    return checklist
