from game import game
import copy

# step one: 5 random outputs
def hill_climb():
    min_iterations_config = game('data/Rushhour6x6_1.csv', 5, 'random', hill_climb = True)
    if 1 in min_iterations_config:
        print(f"Configuration for the first step (step 1):\n{min_iterations_config[1]}")
    else:
        print("First step configuration not found in hill climb configurations.")
    
    # Print configuration for the 50th step
    if 50 in min_iterations_config:
        print(f"\nConfiguration for the 50th step (step 50):\n{min_iterations_config[50]}")
    else:
        print("50th step configuration not found in hill climb configurations.")


hill_climb()