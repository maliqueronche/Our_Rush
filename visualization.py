import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pprint import pprint
import random 


def visualize(dictionary):
    """
    Takes dictionary containing all positions of all vehicles and plots every vehicle onto a grid.
    """
    
    fig, ax = plt.subplots(1)
    ax.axis([0, 6, 0, 6])
    ax.grid(True)
    ax.set_aspect('equal')

    # Loop over vehicles, assign them a color, and plot them
    for ID, value in dictionary.items():
        position = dictionary[ID].position
        
        # Make the objective vehicle red
        if chr(ID) == 'X':
            colour = 'red'
        else: 
            colour = random.choice(list(mcolors.TABLEAU_COLORS.keys()))
        

        # Plot vehicles
        for tup in position:
            ax.plot(tup[0]+0.5, tup[1]+0.5, color=colour, marker='s', markersize=43)
    plt.show()
   

    

        
            
    

            





