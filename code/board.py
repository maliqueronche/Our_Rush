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
  def new_position(self, car_orientation, loc_tup, direction):
    '''
    Generates new position for car instance based on orientation (H or V),
    column/row of postition (loc_tup) and direction (forward or
    backward).
    '''

    row, col = loc_tup

    if car_orientation == 'H':
      if direction == 'forward':
        new_col = col + 1
      else:
        new_col = col - 1
      if -1 < new_col < 6:
        return new_row, new_col
    else:
      if direction == 'forward':
        new_row = row + 1
      else :
        new_row = row - 1
      if -1 < new_row < 6 :
        return new_row, new_col
    return row, col


  def check_availability(self, location):
    '''
    Checks whether there is space for moving, given the location.
    '''
    row, col = location
    if row > self.size or col > self.size:
      return None
    return self.board[row,col]

  # does one move or logs which cars are blocking it's way
  def one_move(self, ID, direction):
    moving_car = self.cars[ID]
    car_front = moving_car.position[-1]
    car_back = moving_car.position[0]
    car_orientation = moving_car.orientation

    if direction in ['left', 'up']:

        #new position based on orientation and desired direction
        new_back = self.new_position(car_orientation, car_back, 'back')

        #check whether new back is availible
        availability_back = self.check_availability(new_back)


        #if availible, move car
        if availability_back == 0:
            moving_car.position.pop()
            moving_car.position.insert(0, new_back)


    elif direction in ['right', 'down']:

        #new position based on orientation and desired direction
        new_front = self.new_position(car_orientation, car_front, 'forward')

        #check whether new front is availible
        availability_front = self.check_availability(new_front)


        #if availible, move car
        if availability_front == 0:

            moving_car.position.pop(0)
            moving_car.position.append(new_front)

    self.place_cars(self.cars)
