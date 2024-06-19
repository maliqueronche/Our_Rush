from game import game
import copy

# step one: 5 random outputs
def hill_climb():

    # compute board position for every step in random iteration, key is step, value is board position
    min_iterations_dict = position_every_step()
    if 1 in min_iterations_dict.keys():
        print(f"Configuration for step 1:\n{min_iterations_dict[1]}")
    else:
        print("First step not found")
    
    if 50 in min_iterations_dict.keys():
        print(f"\nConfiguration for step 50:\n{min_iterations_dict[50]}")
    else:
        print("50th step not found")




def position_every_step():
    iterations, min_iterations_dict = game('data/Rushhour6x6_1.csv', 5, 'random', hill_climb = True)
    # print(min_iterations_config)
    # if 1 in min_iterations_config.keys():
    #     print(f"Configuration for step 1:\n{min_iterations_config[1]}")
    # else:
    #     print("First step not found")
    
    # if 50 in min_iterations_config.keys():
    #     print(f"\nConfiguration for step 50:\n{min_iterations_config[50]}")
    # else:
    #     print("50th step not found")
    return min_iterations_dict

hill_climb()