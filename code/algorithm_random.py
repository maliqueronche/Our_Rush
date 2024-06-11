import board
import classes
import random

# Step 1: randomly select vehicle 
def random_algorithm(vehicles, board):
    random_vehicle, value = random.choice(list(vehicles.items()))
    print(random_vehicle)

    # Step 2: check whether vehicle can make a move
    

