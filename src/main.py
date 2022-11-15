#!/usr/bin/env python3

from life import Game

# Time between generations in milliseconds.
SPEED = 10

def main():
    rand_ratio = float(input("Pourcentage de cellules vivantes: ")) / 100
    height = int(input("Hauteur du tableau en cellules: "))
    width = (height * 3) // 2       # Suitable 3:2 aspect ratio
    cell_size = 1000 // height      # Inverse ratio between cell and window size

    game = Game(width, height, cell_size)
    game.randomise(rand_ratio)
    game.advise_user()
    game.start(SPEED)

if __name__ == "__main__":
    main()
