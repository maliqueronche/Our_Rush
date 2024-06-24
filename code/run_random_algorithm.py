from algorithm_random import Random_algorithm as ra
import classes 


def run_random(hill_climb=False):
        


    if algorithm in ['random', 'hillclimb']:

        # Initiate random step
        random_exp = ra(cars_dict, game_board)

        # track current config
        current_config = {}
        i = 0

        while cars_dict[ord('X')].position != end_position:

            # for hill climb, save new board, every step
            if hill_climb:
                random_exp.random_step(hill_climb = True)
                cars_dict = random_exp.cars
                current_config[i] = random_exp.copy_cars_dict(cars_dict)

                if i > min_iterations:
                    break

            else:
                random_exp.random_step()
            
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
        return min_iterations_config
            


