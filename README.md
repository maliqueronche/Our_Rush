# Our_Rush

## What is Rush-Hour
Rush hour is a game where the objective is to drive a red car out of a busy parking space. The parking space is a grid of 6x6, 9x9 or 12x12. There are two kind of vehicles, a car, which is spaces 2 long, and a truck, which is 3 spaces long. Vehicles are placed on the grid and need to be moved in such a way that the red car can be parked out. Vehicles can only move forward and backward, and can stand horizontally or vertically. The goal is to get the red car out in the least amount of moves, where one move is one movement of a car (can be one, two or more ‘steps’ of a vehicle). 

### Code vs Data vs Results
The git is divided into three parts, the code, the data and the results. Just as the name suggests, our code can be found in the ‘code’ directory, the start positions of cars are in the ‘data’ directory and our results get exported to the ‘results’ directory. 

### Different algorithms. 
In order to solve this problem, we have written different kinds of algorithms. First, a random algorithm, which finds random solutions for the games. Secondly, a breadth first algorithm, which looks for the first combinations of steps that results in a solution. Third, a depth first algorithm, which looks for the first solution it will come across. And lastly, a hill climber, which starts with a random solution and climbs towards a better solution. A more in depth explanations of the algorithms can be found later in this file, under the subheadings for these algorithms. 

### Random algorithm
The first algorithm that can be used to solve the Rush Hour games is a random algorithm. The random algorithm produces a random solution based on the given boards. When running random, a random car and a random direction are chosen. If it is possible to move that car in that direction, the move will be made. If the chosen direction is not available, but the other direction is, the car will be moved into that direction. If the car is not able to move in any direction, a new car will be randomly selected. We repeat this process until the red car arrives at its final destination, a.k.a. when the red car is parked out.

### Breath first algorithm
The second algorithm to solve Rush Hour is a breadth-first search (BFS) algorithm. BFS explores all possible moves systematically to find the shortest path to the solution.Starting with the initial board configuration, the algorithm places it in a queue. It then processes each board configuration by dequeuing it and generating all valid moves for each car in both possible directions. New configurations are added to the queue and recorded to avoid duplicates.The process continues until the red car reaches the exit, at which point the algorithm returns the sequence of moves that led to the solution. By exploring all possible moves and tracking previously encountered configurations, the BFS algorithm ensures an optimal solution to the Rush Hour game.

### Depth first algorithm
The third algorithm to solve Rush Hour is a depth-first search (DFS) algorithm. DFS explores as far as possible along each branch before backtracking to find a solution.Starting with the initial board configuration, the algorithm uses a stack to manage the configurations. It processes each configuration by popping it from the stack and generating all valid moves for each car in both possible directions. New configurations are added to the stack and recorded to avoid duplicates.The algorithm continues this process, diving deep into each possible sequence of moves, until the red car reaches the exit. Upon reaching the exit, the algorithm returns the sequence of moves that led to the solution. By exploring each path deeply and tracking previously encountered configurations, the DFS algorithm aims to find a solution to the Rush Hour game.

### Hill climb algoritm 
The fourth and last algorithm that can be used to solve Rush Hour is a hill climb algorithm. Hill climb starts with a random solution of a game. The algorithm then slices either systematically or randomly and creates slices of a certain size. A begin state (begin of the slice) and an end state (end of the slice) are then established. The goals is to generate a more efficient way to go from the begin state to the end state. This is done by randomly generating ways to go from start to end and selecting the fastest one. This will then be repeated for every slice in the original random solution. This whole process is then repeated multiple times to ensure the solution gets better and better (hill climb).

### How to run
To actually generate results, the game.py file needs to be ran in the terminal, accompanied by some arguments. This is what you would type in the command line: code/game.py <game> <algorithm> <rounds>. For game there are seven options: 1-7 for games 1-7. For algorithm there are four options: random, bfs, dfs and hillclimb. The rounds argument indicates how many times you would like to run the algorithm for that certain game. Note that this argument is optional. If you do not note any argument for 'rounds' the algorithm will run 1 time. 



