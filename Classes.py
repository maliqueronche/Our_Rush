import numpy as np
import matplotlib.colors as mcolors
import random 

class Vehicle():

  # Initialise vehicle
  def __init__(self,ID, orientation, column, row, length):
    """
    Instance contains the following properties:
    - ID: identification of vehicle (2 integers: XX)
    - orientation: the vehicle is either positioned vertically (V) or horizontally (H)
    - column: the first column of occurrence for the vehicle
    - row: the first row of occurrence for the vehicle
    - length: length of the vehicle, (either 2, or 3)
    - position: list containing the position of the vehicle 
    - color: color of the vehicle
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

    if chr(ID) == 'X':
            self.color = 'red'
        else: 
            self.color = random.choice(list(mcolors.TABLEAU_COLORS.keys()))
        



    

