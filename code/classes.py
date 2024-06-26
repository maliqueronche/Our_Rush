import numpy as np
import matplotlib.colors as mcolors
import random

class Vehicle():
    """
    Represents a vehicle in the game. A vehicle can be either horizontal or vertical, and can move within the board.
    """
    
    def __init__(self,ID, orientation, column, row, length):
      """
      Initializes a vehicle with the given properties.

      Args:
          ID (int): The identification of the vehicle.
          orientation (str): The orientation of the vehicle, either 'H' for horizontal or 'V' for vertical.
          column (int): The initial column position of the vehicle.
          row (int): The initial row position of the vehicle.
          length (int): The length of the vehicle, which can be either 2 or 3.
      """
      self.ID = ID
      self.orientation = orientation
      self.column = column -1
      self.row = row -1
      self.length = length
      self.position = []


      # add starting positions to list
      if orientation == 'H':
        for _ in range(self.length):
          self.position.append ((self.row, self.column))
          self.column += 1
      else:
        for _ in range(self.length):
            self.position.append((self.row, self.column))
            self.row +=1

      # assign color to vehicle
      if chr(ID) == ord('X'):
        self.color = 'red'
      else:
        self.color = random.choice(list(mcolors.TABLEAU_COLORS.keys()))

    def change_position(self, direction, orientation):
        """
        Changes the position of the vehicle based on the given direction and orientation.
        """
        new_position = []
        for place in self.position:
          row, col = place

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
            
          new_place = row, col
          new_position.append(new_place)
        self.position = new_position


