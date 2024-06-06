import numpy as np

class Board():
  def __init__(self, size = 6):
    self.size = size
    self.board = np.zeros((size, size))
    print (self.board)

  # Places cars on an empty playing board
  def place_cars(self, cars_dict):
    self.cars = cars_dict

    # Reset board for new position
    self.board = np.zeros((self.size, self.size))
    for id, vehicle in cars_dict.items():
        location = vehicle.position
        for tup in location:
            self.board[tup] = vehicle.ID
    self.start_board = self.board
    print (self.board)

  # Gets the place of one space before (pos) or behind (neg) a car given an orientation (H or V)
  def get_place(self, car_orientation, loc_tup, direction):

    row, col = loc_tup
    if car_orientation == 'H':
      if direction == 'forward':
        col +=1
      else:
        col -= 1
    else:
      if direction == 'forward':
        row += 1
      else :
        row -=1
    return row, col

  # Checks what the space is, given the location
  def check_availability(self, location):
    row, col = location
    if row > self.size or col > self.size:
      return None
    return self.board[row,col]

  # Does one move or logs which cars are blocking its way
  def one_move(self, ID, direction):
    moving_car = self.cars[ID]
    print("before moving", moving_car.position)
    car_front = moving_car.position[-1]
    car_back = moving_car.position[0]
    car_orientation = moving_car.orientation

    if direction in ['left', 'up']:

        # New position based on orientation and desired direction
        new_back = self.get_place(car_orientation, car_back, 'back')

        # Check whether new back is available
        availability_back = self.check_availability(new_back)


        # If space available, move car
        if availability_back == 0:
            moving_car.position.pop()
            moving_car.position.insert(0, new_back)
      
           

    elif direction in ['right', 'down']:

        # New position based on orientation and desired direction
        new_front = self.get_place(car_orientation, car_front, 'forward')
        
        # Check whether new front is available
        availability_front = self.check_availability(new_front)

        # If space available, move car
        if availability_front == 0:
          moving_car.position.pop(0)
          moving_car.position.append(new_front)
          

          

    self.place_cars(self.cars)
