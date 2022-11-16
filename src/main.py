#!/usr/bin/env python3

from life import Game

# Default values
RAND_RATIO = 0.15
HEIGHT = 100

# Time between generations in milliseconds.
SPEED = 20

def get_height() -> int:
    '''
    Returns the height of the board in cells to be used.
    '''
    line = input(f"Hauteur du tableau en cellules (par défaut: {HEIGHT}): ")

    if line == '':
        return HEIGHT
    else:
        return int(line)

def get_rand_ratio() -> int:
    '''
    Returns the randomisation ratio of the board to be used.
    '''
    line = input(f"Pourcentage de cellules vivantes (par défaut: {round(RAND_RATIO * 100)}): ")

    if line == '':
        return RAND_RATIO
    else:
        return float(line) / 100

def main():
    height = get_height()
    rand_ratio = get_rand_ratio()
    width = (height * 3) // 2       # Suitable 3:2 aspect ratio
    cell_size = 1000 // height      # Inverse ratio between cell and window size

    game = Game(width, height, cell_size)
    game.randomise(rand_ratio)
    game.user_edit()
    game.start(SPEED)

if __name__ == "__main__":
    main()
