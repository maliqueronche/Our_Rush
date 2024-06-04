import numpy as np

class Vehicle():
  def __init__(self, rotation, column, row, length):
    self.rotation = rotation
    self.column = column -1
    self.row = row -1
    self.lenght = length
    self.position = []

    if rotation == H:
      for _ in self.lenght:
        self.position.append (self.row, self.column)
        self.column += 1
    else :
      for _ in self.lenght:
          self.position.append(self.row, self.column)
          self.row +=1 


class Board():
  def __init__(self, size = 6):
    self.size = size
    self.board = np.zeros((size, size))
    print (self.board)

class Game():
  def __init__(self. )

    

