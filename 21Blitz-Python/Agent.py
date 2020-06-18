import numpy as np
import random as rand
from Card import Card

class State:

    def __init__(self, stacks, top):
        self.stacks = stacks
        self.top = top



class Agent:
    """AI agent to train for our game
    
    Action Space:
        0 - undo
        1 - stack 1
        2 - stack 2
        3 - stack 3
        4 - stack 4
    
    """

    def __init__(self):
        self.q_table = np.zero([1, 5])
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        self.states = []

    def choose(self, state):
        if rand.uniform(0, 1) < self.epsilon:
            return rand.randint(0, 4)
        else:
            return np.argmax(self.q_table[state])

    #def find_state(self, stacks, card):



    