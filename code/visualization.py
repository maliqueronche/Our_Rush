import matplotlib.pyplot as plt
from pprint import pprint


def visualize(dictionary, board):
    """
    Takes dictionary containing all positions of all vehicles and plots every
    vehicle onto a grid.
    """
    # Create subplots
    fig, ax = plt.subplots(1)

    # Set axis, grid and aspect
    ax.axis([0, board.size, board.size, 0])
    ax.grid(True)
    ax.set_aspect('equal')

    # Loop over vehicles, and plot them
    for ID, value in dictionary.items():
        position = dictionary[ID].position

        # Plot vehicles
        for tup in position:
            ax.plot(tup[1]+0.5, tup[0]+0.5, color=dictionary[ID].color, marker='s', markersize=43)
    plt.show(block=False)
    plt.pause(0.1)
    plt.close()
