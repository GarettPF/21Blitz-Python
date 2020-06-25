"""

    Author: Garett Pascual-Folster
    Date: 6/14/2020
    Description: A replica of the game 21 Blitz on mobile

"""

from Agent import State, Agent
from Game import Game
from os import system


def play(episode):
    agent = Agent()
    agent.load_data()
    game = Game()
    while not game.GameOver:
        # display
        system('cls')
        print("Game: ", episode)
        game.print()

        # choose
        stateNum = agent.find_state(game.stack, game.top)
        choice = agent.choose(stateNum)
        game.choose(choice)

        #update game and agent
        busted = game.update()
        nextState = agent.find_state(game.stack, game.top)
        agent.update(stateNum, nextState, choice, game.points, busted)

    game.record()
    agent.save_data()


def main():
    episode = 0
    episodes = 250

    for i in range(episodes):
        play(i)
    
    print("Finished training :)")


if __name__ == "__main__":
    main()