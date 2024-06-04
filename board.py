import numpy as np

class Board():
  def __init__(self, size = 6):
    self.size = size
    self.board = np.zeros((size, size))
    print (self.board)
  
  def place_cars(self, cars_dict):
    self.cars = cars_dict
    for id, vehicle in cars_dict.items():
        location = vehicle.position
        for tup in location:
            self.board[tup] = vehicle.ID
    print (self.board)

  def one_move(self, ID):
    moving_car = self.cars[ID]
    red_front = red_car.position[-1]
    red_back = red_car.position[0]

    if 
     
    pass

    