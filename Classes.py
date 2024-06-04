import numpy as np

class Vehicle():
  def __init__(self,ID, rotation, column, row, length):
    self.ID = ID
    self.rotation = rotation
    self.column = column -1
    self.row = row -1
    self.lenght = length
    self.position = []

    if rotation == 'H':
      for _ in range(self.lenght):
        self.position.append ((self.row, self.column))
        self.column += 1
    else :
      for _ in range(self.lenght):
          self.position.append((self.row, self.column))
          self.row +=1 



    

