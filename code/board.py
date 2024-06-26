import numpy as np
import classes

class Board():
  """
  Board class creates board instance:
  - Initialise board with given size
  - Places car instances on empty playing board
  - creates the start positions

  """
  def __init__(self, cars_dict, size = 6):
    """
    Initializes the Board with cars and size.
      
    Args:
        cars_dict (dict): Dictionary containing car instances.
        size (int): The size of the board (default is 6).
    """
    self.size = size
    self.cars = cars_dict
    self.board = np.zeros((size, size))

    for id, vehicle in self.cars.items():
        if type(vehicle) == classes.Vehicle:
          location = vehicle.position
          for tup in location:
              self.board[tup] = vehicle.ID
    
        elif type(vehicle) == dict:
          location = cars_dict[id]['position']
          for tup in location:
              self.board[tup] = id
    

  def get_new_pos(self, car_tup, direction, orientation):
    """
    Receives a tuple for location and a direction, then moves the tuple one place.
    
    Args:
        car_tup (tuple): Current position of the car.
        direction (str): Direction to move ('pos' or 'neg').
        orientation (str): Orientation of the car ('H' or 'V').
    
    Returns:
        tuple: New position of the car.
    """    
    
    row, col = car_tup

    if orientation == 'H':
      if direction == 'pos':
        col += 1
      elif direction == 'neg':
        col -= 1
    elif orientation == 'V':
      if direction == 'pos':
        row +=1
      elif direction == 'neg':
        row -= 1

    return row, col

  def move_car(self, car_id, direction):
    """
    Receives a car_id with direction and moves this car across the board.
    
    Args:
        car_id (int): The ID of the car to move.
        direction (str): The direction to move ('pos' or 'neg').
    """    
    new_positions = []
    car = self.cars[car_id]
    positions = car.position
    orientation = car.orientation

    for car_tup in positions:
      new_pos = self.get_new_pos(car_tup, direction, orientation)
      new_positions.append(new_pos)

    for old_pos in positions:
      self.board[old_pos] = 0
    
    for new_pos in new_positions:
      self.board[new_pos] = car.ID

      

     
