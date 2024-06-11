import numpy as np

class Board():
  """
  Board class creates board instance:
  - Initialise board with given size
  - Places car instances on empty playing board
  - creates the start positions

  """
  def __init__(self, cars_dict, size = 6,):
    self.size = size
    self.cars = cars_dict
    self.board = np.zeros((size, size))

    for id, vehicle in self.cars.items():
        location = vehicle.position
        for tup in location:
            self.board[tup] = vehicle.ID
    print (self.board)

  def get_new_pos(car_tup, direction):
    row, col = car_tup

    if direction == 'up':
      row -= 1
    if direction == 'down':
      row += 1
    if direction == 'left':
      col -= 1
    if direction == 'right':
      col +=1

    return row, col

  def move_car(car_id, direction):
    new_positions = []
    positions = car.positions
    car = self.cars[car_id]

    for car_tup in positions:
      new_pos = get_new_pos(car_tup, direction)
      new_positions.append (new_pos)

    for old_pos in positions:
      self.board[old_pos] = 0
    
    for new_pos in new_positions:
      self.board[new_pos] = car.ID
      

     
