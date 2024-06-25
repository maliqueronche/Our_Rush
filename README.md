# Our_Rush

## What is Rush-Hour
This is code for an algorithm to find the best solution for the game Rush-Hour. Rush hour is a game where the objective is to drive a red car out of a busy parking space. The parking space is a grid of 6x6, 9x9 or 12x12. There are two kind of vehicles, a car, which is 2 long, and a truck, which is 3 long. Vehicles can only move forward and backward, and can stand horizontally or vertically. The goal is to get the red car out in the least amount of moves, where one move is one movement of a car (can be one, two or more ‘steps’ of a vehicle). 

### How to run

### Different algorithms. 
We have tried different kinds of algorithms. First, we have the random algorithm, which finds random solutions to the boards. Second, we have a breadth first algorithm, which looks for the first combinations of steps that find a solution. Third, we made a depth first, which looks for the first solution it will come across. Lastly, we made a hill climber, which starts with a random solution and climbs towards the best solution. More in depth explanations of the algorithms will be under the code for these algorithms. 

### Code vs Data vs Results
The git is divided into three parts, the code, the data and the results. Just as the name suggests, our code is in the map ‘code’, our start positions of cars are in ‘data’ and our results get exported to ‘results’. 

# Code
In de repository there are a lot of files, including the different algorithms, class files, helper files and running files. 

## Classes

### classes.py
This file contains the class ‘Vehicle’, which creates a vehicle with the properties ID, orientation, column, row, length. These properties were given in the input data. Then, position is added to the vehicle. It has the function ‘change_position’ that uses the direction and orientation to move a car over the board. 
ID: this is an integer representing the Unicode of the character corresponding to the car given in the input data. We used an integer to be able to place the ID into a board (see class board). 
Orientation: this is ‘H’ for horizontal and ‘V’ for vertical. This is used do determine whether cars can move up and down, or left and right. It is also used to place cars on a board (see class board). 
Column: this is an integer of the column where the car stands. It is minus 1 compared to the input data because a numpy matrix starts from 0 instead of 1. 
Row: this is an integer of the row where the car stands. It is minus 1 compared to the input data because a numpy matrix starts from 0 instead of 1.
Length: this is 2 or 3, corresponding to a car or truck respectively. 
Position: this is a list of two tuples corresponding to the places that the car uses, for example [(1,1),(1,2)]. 
Change_position(self, direction, orientation): the direction can be ‘pos’ for positive, meaning down or right on the board, or ‘neg’ for negative, meaning up or left on the board. The direction is either ‘H’ or ‘V’ to determine whether the column or the row gets changed.  

### board.py
This class gets a dictionary of cars and a board size and makes a numpy matrix representing a gameboard. It then places all the cars from the dictionary into the board. It has the properties size, cars and board. It has the functions get_new_pos() and move_car(). 
Size: this is an integer that regulates the size of the board. 
Cars: this is the dictionary of the in the board. 
Board: this is the numpy matrix, starting with all zeros, and after the cars are added, the integers representing the cars are in the matrix. 
Get_new_pos(self, car_tup, direction, orientation): it receives a tuple of position, an orientation and a direction and returns a tuple of position changed one step, calculated with the orientation and direction. 
Move_car(self, car_id, direction): moves the car with the car_id one step in the direction. 

## Algorithms

### algorithm_random.py

