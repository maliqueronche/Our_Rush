import matplotlib.pyplot as plt
from pprint import pprint
import random 


def visualize(dictionary):

    
    fig, ax1 = plt.subplots(1)
    ax1.axis([0, 6, 0, 6])
    ax1.grid(True)
    ax1.set_aspect('equal')

    

    for ID, value in dictionary.items():
        position = dictionary[ID].position
        
        if chr(ID) == 'X':
            colour = 'red'
        else: 
            colour = random.choice(['blue', 'green', 'yellow', 'purple', 'brown'])

        # Plot vehicles
        for tup in position:
            ax1.plot(tup[0]+0.5, tup[1]+0.5, color=colour, marker='s', markersize=43)
    plt.show()
   

    

        
            
    

            





