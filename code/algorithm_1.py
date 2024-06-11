

# Step 1: determine which cars need to move in order to get the red car out. 
#         In terms of distance, this means that there is a certain distance 
#         for the red car to move from its starting position to its ending 
#         position. Just like with the "count wrong tiles problem" you can 
#         count the number of cars that are in the way and add "moves". 
#         You can then, like the A-star algorithm, compute the minimum number of 
#         moves needed to solve the game. All cars that in some way block the
#         red car from getting to the exit have to move at least once. 

# TODO: implement

# Step 2: Loop over vehicles and list all possible board configurations for one move.
#         - keep track of which board configurations are already used, 
#           so that the algorithm doesn't play moves that end up in configurations it has already seen.
#         - Only play moves that reduce/retain the number of moves to do.

# TODO: implement

# Step 3: Use a random, breadth, depth, A*, or other algorithm to search through the state-space.

# TODO: implement


