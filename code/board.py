import numpy as np

class Board():
  """
  Board class creates board instance:
  - Initialise board with given size
  - Places car instances on empty playing board
  -

  """
  def __init__(self, size = 6):
    self.size = size
    self.board = np.zeros((size, size))


  def place_cars(self, cars_dict):
    '''
    Places cars on an empty playing board
    '''
    self.cars = cars_dict

    # Reset board for new position
    self.board = np.zeros((self.size, self.size))
    for id, vehicle in cars_dict.items():
        location = vehicle.position
        for tup in location:
            self.board[tup] = vehicle.ID
    self.start_board = self.board
    print (self.board)

  # Takes place of space before (pos) or behind (neg) a car given orientation (H or V)
  def new_position(self, car_orientation, positions, direction):
    '''
    Generates new position for car instance based on orientation (H or V),
    column/row of postition (loc_tup) and direction (forward or
    backward).
    '''

    new_positions = []

    if car_orientation == 'H':
      if direction == 'right':
        for position in positions:
          row, col = position
          new_col = col + 1
          if -1 < new_col < 6:
            new_positions.append((row, new_col))
          else:
            return positions
      else:
        for position in positions:
          row, col = position
          new_col = col - 1
          if -1 < new_col < 6:
            new_positions.append((row, new_col))
          else:
            return positions

    else:
      if direction == 'down':
        for position in positions:
          row, col = position
          new_row = row + 1
          if -1 < new_row < 6:
              new_positions.append((new_row, col))
          else:
            return positions
        
      else :
        for position in positions:
          row, col = position
          new_row = row - 1
          if -1 < new_row < 6:
              new_positions.append((new_row, col))
          else:
            return positions
        
    return new_positions


  def check_availability(self, location, direction):
    '''
    Checks whether there is space for moving, given the location.
    '''

    if direction in ['right, down']:
      row, col = location[-1]
    else:
      row, col = location[0]

    return self.board[row,col]

  # does one move or logs which cars are blocking it's way
  def one_move(self, ID, direction):
    moving_car = self.cars[ID]
    
    #new position based on orientation and desired direction
    new_positions = self.new_position(moving_car.orientation, moving_car.position, direction)

    #check whether new back is availible
    availability_position = self.check_availability(new_positions, direction)

    #if availible, move car
    if availability_position == 0:
      moving_car.position = new_positions


    self.place_cars(self.cars)
