from Card import Card
import random
import time
import copy

class Game:
    """Replica of the 21 Blitz Game"""

    def __init__(self):
        self.GameOver = False
        self.points = 0
        self.busts = 0
        self.deck = []
        self.stack = [[] for _ in range(4)]
        self.shuffle()
        self.size = len(self.deck)
        self.top = self.deck[-1]
        self.current = (self.points, self.busts, self.deck, self.size, self.top, self.stack)
        self.undo = copy.deepcopy(self.current)
        self.startTime = time.perf_counter()


    def shuffle(self):
        suites = ('s','c','h','d')
        deck_check = [[False for _ in range(13)] for _ in range(4)]

        while not len(self.deck) == 52:
            while True:
                v = random.randint(0, 12)
                s = random.randint(0, 3)
                if not deck_check[s][v]:
                    deck_check[s][v] = True
                    break
            card = Card(suites[s], v+1)
            self.deck.append(card)

    def choose(self, c):
        #c = -1
        #while c < 0 or c > 4:
        #    c = int(input("Choose a stack (1-4, 0 for undo): "))
        
        if c == 0:
            self.points = self.undo[0]
            self.busts = self.undo[1]
            self.deck = self.undo[2]
            self.size = self.undo[3]
            self.top = self.undo[4]
            self.stack = self.undo[5]
            self.current = copy.deepcopy(self.undo)
        else:
            # save gamestate before changes
            self.undo = copy.deepcopy(self.current)

            # next gamestate
            self.stack[c-1].append(self.top)
            self.deck.pop()
            self.size = len(self.deck)
            if (self.size == 0):
                self.GameOver = True
                return
            self.top = self.deck[-1]
            self.current = (self.points, self.busts, self.deck, self.size, self.top, self.stack)


    def results(self, sum, size, ace, wild):
        clear = False
        if wild:
            self.points += 200
            clear = True
            if size == 5:
                self.points += 600
        elif (ace and sum > 20) or (sum > 21):
            self.busts += 1
            clear = True

        if (ace and sum == 20) or (ace and sum == 10) or (sum == 21):
            self.points += 400
            clear = True
            if size == 5:
                self.points += 600

        if not clear and size == 5:
            self.points += 600
            clear = True

        return clear

    def clearStack(self, stack):
        while len(stack) != 0:
            stack.pop()

    def update(self):
        busts = self.busts
        for s in self.stack:
            sum = 0
            Ace = Wild = False

            for c in range(len(s)):
                val = 0
                if s[c].value > 10:
                    val = 10
                elif s[c].value == 1:
                    Ace = True
                else:
                    val = s[c].value
                Wild = s[c].isWild()
                sum += val

            if (self.results(sum, len(s), Ace, Wild)):
                self.clearStack(s)

        if self.busts == 3 or time.perf_counter() - self.startTime >= 3*60:
            self.GameOver = True

        return True if self.busts - busts != 0 else False


    def record(self):
        len = time.perf_counter() - self.startTime
        min = int(len // 60)
        sec = int(len % 60)

        file = open("results.csv", "a")
        results = str(self.points) + ', ' + str(min) + ':'
        results += '0' if sec < 10 else ''
        results += str(sec) + ', ' + str(self.busts) + ', ' + str(self.size)
        print(results)
        file.write(results + '\n')
        file.close()

    def print(self):
        display = ('A','2','3','4','5','6','7','8','9','T','J','Q','K')
        print("Busts: ", self.busts)
        curTime = time.perf_counter() - self.startTime
        min = int(curTime // 60)
        sec = int(curTime % 60)
        strTime = str(min) + ':'
        strTime += '0' if sec<10 else '' 
        strTime += str(sec)
        print("Time: " + strTime)
        print("POINTS: ", self.points)
        print("S1   S2   S3   S4")

        for c in range(5):
            print_str = ""
            for s in self.stack:
                try:
                    print_str += s[c].__str__()
                    print_str += "   "
                except:
                    print_str += "--   "
            print(print_str)

        print("Current Card: ", self.top)
        print("Cards Left: ", self.size)
