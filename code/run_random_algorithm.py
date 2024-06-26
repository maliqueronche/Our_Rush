from algorithm_random import Random_algorithm as ra
import pandas as pd
import numpy as np
import board
import classes

def run_random(filepath, rounds, algorithm, size, end_position, hill_climb=False):
        
    cars = pd.read_csv(filepath) 
    iterations_list = []
    mean_i = 0
    round = 1
    min_iterations = 10000
    min_iterations_config = {}
    car_moves = []
    for _ in range(rounds):
        
        cars_dict = {}
        # Loop over cars dataframe, create vehicles and store them in dictionary
        for idx, row in cars.iterrows():
            ID = 0
            for letter in row['car']:
                ID += ord(letter)
            vehicle = classes.Vehicle(ID, row['orientation'], row['col'], row['row'], row['length'])
            cars_dict[ID] = vehicle

        # Initialise board and add cars in starting positions
        game_board = board.Board(cars_dict, size)
    
        if algorithm in ['random']:
        # Initiate random step
            random_exp = ra(cars_dict, game_board)

            # track current config
            current_config = {}
            i = 0

            while cars_dict[ord('X')].position != end_position:

                # for hill climb, save new board, every step
                if hill_climb:
                    car_move = random_exp.random_step(hill_climb=True)
                    cars_dict = random_exp.cars
                    current_config[i] = random_exp.copy_cars_dict(cars_dict)
                    car_moves.append(car_move)
                    if i > min_iterations:
                        break

                else:
                    car_moves.append(random_exp.random_step())
                
                i +=1
                
                
            # print(f"Round {round}, Iterations: {i}, Min Iterations: {min_iterations}")

            # Save the amount of iterations and use it to calculate the mean
            iterations_list.append(i)
            mean_i += i
            if round % 100 == 0:
                end = time()
                print(f'The time elapsed: {end-start:.2f} seconds.')
                print(f"progress:{(round/rounds) * 100}")
                start = time()
            round += 1

            if hill_climb and i < min_iterations:
                min_iterations = i
                min_iterations_config = random_exp.copy_cars_dict(current_config)


    if hill_climb:

        return min_iterations_config, car_moves
    else:
        return car_moves


