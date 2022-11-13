#!/usr/bin/env python3

from life import Game

def main():
    game = Game(150, 100, 8)
    game.advise_user()
    game.start(100)

if __name__ == "__main__":
    main()
