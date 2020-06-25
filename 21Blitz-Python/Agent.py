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

    def __str__(self):
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

    def load(self, data):
        stack = 0
        card = 0
        for v in range(0, len(data)-3, 2):
            self.stacks[stack][card] = int(data[v:v+2])
            stack = stack+1 if card == 4 else stack
            card = 0 if card == 4 else card+1
        self.top = int(data[20:22])

      



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
        self.q_table = []
        self.alpha = 0.4
        self.gamma = 0.8
        self.epsilon = 0.8
        self.states = []
        self.points = 0

    def choose(self, state):
        if rand.uniform(0, 1) <= self.epsilon:
            return rand.randint(0, 4)
        else:
            return self.q_table[state].index(max(self.q_table[state]))

    def update(self, cur_state, next_state, action, points, busted):
        old_value = self.q_table[cur_state][action]
        next_max = max(self.q_table[next_state])
        reward = self.calc_reward(points, busted)

        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[cur_state][action] = new_value

    def calc_reward(self, points, busted):
        change = points - self.points
        if busted:
            return -10
        elif change == 0:
            return -1
        else:
            return (change // 100)

    def find_state(self, stacks, top):
        search_state = State(stacks, top).__str__()

        for i in range(len(self.states)):
            state = self.states[i].__str__()
            if (state == search_state):
                return i

        newState = State(stacks, top)
        self.states.append(newState)
        self.q_table.append([0 for _ in range(5)])
        return len(self.q_table) - 1

    def save_data(self):
        with open("state_table.csv", "w") as f:
            for state in self.states:
                f.write(state.__str__())
                f.write('\n')

        with open("q_table.csv", "w") as f:
            for value in self.q_table:
                for v in value:
                    f.write(str(v) + ",")
                f.write('\n')

    def load_data(self):
        with open("state_table.csv", "r") as f:
            for line in f:
                state = State([[]], Card('', 0))
                state.load(line)
                self.states.append(state)

        with open("q_table.csv", "r") as f:
            for line in f:
                values = line.split(',')
                new_values = []
                for v in range(len(values)-1):
                    new_values.append(float(values[v]))
                self.q_table.append(new_values)

    