import random as rand
from Card import Card

class State:

    def __init__(self, stacks, top):
        self.stacks = [[0]*5 for _ in range(4)]
        for stack in range(4):
            for card in range(5):
                try:
                    val = stacks[stack][card].value
                except:
                    val = 0
                self.stacks[stack][card] = val
        self.top = top.value

    def str(self):
        return_str = ""
        for s in range(4):
            for c in range(5):
                try:
                    card = self.stacks[s][c]
                    return_str += str(card).zfill(2)
                except:
                    return_str += "".zfill(2)
        return_str += str(self.top).zfill(2)
        return return_str


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
        self.q_table = {}
        self.alpha = 0.4
        self.gamma = 0.8
        self.epsilon = 0.3
        self.points = 0

    def choose(self, stack, top):
        state = self.find_state(stack, top)
        self.state = state
        if rand.uniform(0, 1) <= self.epsilon:
            return rand.randint(0, 4)
        else:
            return self.q_table[state].index(max(self.q_table[state]))

    def find_state(self, stacks, top):
        search = State(stacks, top).str()

        if search not in self.q_table:
            self.q_table[search] = [0] * 5
        return search

    def update(self, next, action, points, busted):
        reward = self.calc_reward(points, busted)
        old_v = self.q_table[self.state][action]
        next_m = max(self.q_table[next])

        new_v = old_v*(1 - self.alpha) + self.alpha*(reward + (self.gamma * next_m))
        self.q_table[self.state][action] = new_v

    def calc_reward(self, points, busted):
        change = points - self.points
        if busted:
            return -10
        elif change == 0:
            return -1
        else:
            return (change // 100)

    def save_data(self):
        with open("q_table.csv", "w") as f:
            for state, actions in self.q_table.items():
                f.write(state + ',')
                for a in actions: 
                    f.write(str(a) + ',')
                f.write('\n')

    def load_data(self):
        with open("q_table.csv", "r") as f:
            for line in f:
                values = line.split(',')
                key = values[0]
                new_values = []
                for v in range(1, len(values)-1):
                    new_values.append(float(values[v]))
                self.q_table[key] = new_values

    