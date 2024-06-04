import numpy as np

class Board():
  def __init__(self, size = 6):
    self.size = size
    self.board = np.zeros((size, size))
    print (self.board)
  
  # Places cars on an empty playing board
  def place_cars(self, cars_dict):
    self.cars = cars_dict
    for id, vehicle in cars_dict.items():
        location = vehicle.position
        for tup in location:
            self.board[tup] = vehicle.ID
    self.start_board = self.board
    print (self.board)

  # Gets the place of one space before (pos) or behind (neg) a car given a rotation (H or V)
  def get_place(self, car_rotation, loc_tup, side)

    row, col = loc_tup
    if car_rotation == 'H':
       if side == 'pos':
          col +=1
        else: 
          col -= 1
    else :
       if side == 'pos':
          row += 1
       else :
          row -=1
    return row,col
  
  # Checks what the space is given the location
  def check_availability(self, location):
    row, col = location
    if row > self.size or col > self.size:
      return None
    return self.board[row,col]
  
  # does one move or reports which cars are blocking it's way
  def one_move(self, ID):
    moving_car = self.cars[ID]
    car_front = moving_car.position[-1]
    car_back = moving_car.position[0]
    car_rotation = moving_car.rotation

    new_front = self.get_place(car_rotation, car_front, 'front')
    new_back = self.get_place(car_rotation, car_back, 'back')

    availability_front = self.check_availability(new_front)
    availability_back = self.check_availability(new_back)
    