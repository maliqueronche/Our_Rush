from game import game

# step one: 5 random outputs
ten_iterations = game('data/Rushhour6x6_1.csv', 5, 'random', hill_climb = True)
iterations = min(ten_iterations)

