"""

    Author: Garett Pascual-Folster
    Date: 6/14/2020
    Description: A replica of the game 21 Blitz on mobile

"""

from Game import Game
from os import system

def main():

    game = Game()
    while not game.GameOver:
        system('cls')
        game.print()
        game.choose()
        game.update()

    system('cls')
    game.record()
    print("Game over :(")


if __name__ == "__main__":
    main()