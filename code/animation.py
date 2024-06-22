import pygame
import sys
import time
import pandas as pd
import random

def animate(board_file, result_file, size):
    """Animate takes three files, one this the original board, one with the 
    results to solve the board and the size of the board. It then makes an 
    animation based on the received information."""
def animate(board_file, result_file, size):
    """Animate takes three files, one this the original board, one with the 
    results to solve the board and the size of the board. It then makes an 
    animation based on the received information."""

    # initialize pygame
    pygame.init()

    # create grid
    screen_width, screen_height = 600, 600

    # initiate grid, cell and border size
    # initiate grid, cell and border size
    if size == 6:
        grid_size = 6 
    elif size == 9:
        grid_size = 9
    elif size == 12:
        grid_size = 12
    
    cell_size = screen_width // grid_size

    border_size = 50

    # display screen
    screen = pygame.display.set_mode((screen_width + 2 * border_size, screen_height + 2 * border_size))
    border_size = 50

    # display screen
    screen = pygame.display.set_mode((screen_width + 2 * border_size, screen_height + 2 * border_size))
    pygame.display.set_caption('Rush Hour')

    background_colour = (100, 100, 100) 
    clock = pygame.time.Clock()

    # load cars and steps
    cars = load_start_board(board_file)
    steps = load_steps(result_file)
    # load cars and steps
    cars = load_start_board(board_file)
    steps = load_steps(result_file)

    step_count = 0

    font = pygame.font.SysFont(None, 36)

    font = pygame.font.SysFont(None, 36)

    while True:

        # keep 'playing' until quit

        # keep 'playing' until quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(background_colour)

        # count steps
        # count steps
        if step_count < len(steps):
            car_id, distance = steps[step_count]
            cars[car_id].move_car(distance)
            step_count += 1

        # draw border
        pygame.draw.rect(screen, (0, 0, 0), (border_size, border_size, screen_width, screen_height), 5)

        # draw cars
        # draw border
        pygame.draw.rect(screen, (0, 0, 0), (border_size, border_size, screen_width, screen_height), 5)

        # draw cars
        for car in cars.values():
            car.draw_car(screen, cell_size, border_size)

        # display moves
        counter_text = font.render(f'Moves: {step_count}', True, (255, 255, 255))
        screen.blit(counter_text, (10, 10))
            car.draw_car(screen, cell_size, border_size)

        # display moves
        counter_text = font.render(f'Moves: {step_count}', True, (255, 255, 255))
        screen.blit(counter_text, (10, 10))

        pygame.display.flip()
        clock.tick(8)  
        time.sleep(0.005)

def load_start_board(file_path):
    """Imports initial start board from csv and turns it into dictionary"""


    start_data = pd.read_csv(file_path)
    cars = {}
    taken_colours = set()
    red_car_colour = (255, 0, 0)


    for row, column in start_data.iterrows():
        car_id = column['car']
        orientation = column['orientation']
        col = column['col'] - 1
        row = column['row'] - 1
        length = column['length']
        position = (col, row)


        if car_id == 'X':
            colour = red_car_colour
        else:
            colour = get_unique_colours(taken_colours)
            taken_colours.add(colour)


        cars[car_id] = car(car_id, colour, position, orientation, length)

    return cars

def get_unique_colours(taken_colours):
    """Makes sure there are only unique colours on the board"""
    """Makes sure there are only unique colours on the board"""

    while True:
        colour = tuple(random.randint(0, 255) for _ in range(3))
        if colour not in taken_colours:
            return colour

def load_steps(file_path):
    """Loads steps from csv"""

    """Loads steps from csv"""

    steps_df = pd.read_csv(file_path)
    steps = []


    for row, column in steps_df.iterrows():
        car_id = column['car']
        move = column['move']
        steps.append((car_id, move))


    return steps

class car:
    '''
    Car class creates car instance. Init initializes properties that
    belong to a car instance, draw_car puts the car on the grid, 
    move_car actually moves car instance given steps.
    '''
    def __init__(self, id, colour, position, orientation, length):
        self.id = id
        self.colour = colour
        self. position = position
        self.orientation = orientation
        self.length = length

    def draw_car(self, screen, cell_size, border_size):
        """Draws car based in screen, cell size and border size"""

    def draw_car(self, screen, cell_size, border_size):
        """Draws car based in screen, cell size and border size"""

        x, y = self.position

        # main car rectangle
        if self.orientation == 'H':
            pygame.draw.rect(screen, self.colour, (x * cell_size + border_size, y * cell_size + border_size, self.length * cell_size, cell_size), border_radius = 40)
            pygame.draw.rect(screen, self.colour, (x * cell_size + border_size, y * cell_size + border_size, self.length * cell_size, cell_size), border_radius = 40)
        else:
            pygame.draw.rect(screen, self.colour, (x * cell_size + border_size, y * cell_size + border_size, cell_size, self.length * cell_size), border_radius = 40)
            pygame.draw.rect(screen, self.colour, (x * cell_size + border_size, y * cell_size + border_size, cell_size, self.length * cell_size), border_radius = 40)

        # car roof
        roof_colour = tuple(max(0, c - 50) for c in self.colour)
        if self.orientation == 'H':
            pygame.draw.rect(screen, roof_colour, (x * cell_size + border_size + cell_size // 4, y * cell_size + border_size + cell_size // 4, self.length * cell_size - cell_size // 2, cell_size // 2))
            pygame.draw.rect(screen, roof_colour, (x * cell_size + border_size + cell_size // 4, y * cell_size + border_size + cell_size // 4, self.length * cell_size - cell_size // 2, cell_size // 2))
        else:
            pygame.draw.rect(screen, roof_colour, (x * cell_size + border_size + cell_size // 4, y * cell_size + border_size + cell_size // 4, cell_size // 2, self.length * cell_size - cell_size // 2))
            pygame.draw.rect(screen, roof_colour, (x * cell_size + border_size + cell_size // 4, y * cell_size + border_size + cell_size // 4, cell_size // 2, self.length * cell_size - cell_size // 2))

    def move_car(self, steps):
        """Moves car based on steps"""
        
        """Moves car based on steps"""
        
        x, y = self.position
        if self.orientation == 'H':
            self.position = (x + steps, y)
        else:
            self.position = (x, y + steps)
 
if __name__ == '__main__':
    size = 9
    board_file = 'data/Rushhour9x9_4.csv'
    result_file = 'results/bfs_9x9_4_1.csv'
    animate(board_file, result_file, size)