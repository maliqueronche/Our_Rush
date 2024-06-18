import numpy as np
import classes

class Board():
  """
  Board class creates board instance:
  - Initialise board with given size
  - Places car instances on empty playing board
  - creates the start positions

  """
  def __init__(self, cars_dict, size=6):
    self.size = size
    self.cars = cars_dict
    self.board = np.zeros((size, size))

    for id, vehicle in self.cars.items():
        if type(vehicle) == classes.Vehicle:
          location = vehicle.position
          for tup in location:
              self.board[tup] = vehicle.ID
    
        if type(vehicle) == dict:
          # print ('this is a dict')
          location = cars_dict[id]['position']
          for tup in location:
              self.board[tup] = id
    


    # print (self.board)

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

  def move_car(self, car_id, direction):
    '''recieves a car_id with direction and moves this car across the board'''
    new_positions = []
    car = self.cars[car_id]
    positions = car.position
    orientation = car.orientation
    # print (car_id)

    for car_tup in positions:
      new_pos = self.get_new_pos(car_tup, direction, orientation)
      new_positions.append (new_pos)

    for old_pos in positions:
      self.board[old_pos] = 0
    
    for new_pos in new_positions:
      self.board[new_pos] = car.ID

    # print (self.board)
      

     
