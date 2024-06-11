from visualization import visualize


def user_input(cars_dict, game_board):
    '''
    The user_input function takes a car dictionary and game_board. The function
    asks a player for input and makes a move based on the inputself.
    The function will keep asking for input until the player quits.
    '''

    keep_playing = True
    while keep_playing:
        move_input = input("Enter move (ID direction) or 'q' to quit: ").split()
        if len(move_input) == 1 and move_input[0].lower() == 'q':
            keep_playing = False

        # If input is correctly formatted, make a move
        elif len(move_input) != 2:
            print("Invalid input. Enter move as 'ID direction' or 'q' to quit.")
        else:
            move_id, direction = move_input
            if not move_id.isdigit():
                print("Invalid ID. ID should be a number.")
            else:
                ID = int(move_id)
                if direction.lower() not in ['left', 'right', 'up', 'down']:
                    print("Invalid direction. Use 'left', 'right', 'up', or 'down'.")
                else:
                    game_board.one_move(ID, direction.lower())
                    visualize(cars_dict, game_board)
