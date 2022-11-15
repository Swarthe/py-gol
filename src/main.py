#!/usr/bin/env python3

from life import Game

def main():
    randcells = int(input("Please enter number of starting alive cells."))
    game = Game(150, 100, 8, randcells)
    game.advise_user()
    game.start(6)

if __name__ == "__main__":
    main()
