import numpy as np
import random
import hashlib

# Check for empty places on board


class Player:
    def __init__(self, indicator):
        self.indicator = indicator

    # Select a random place for the player

    def choose_action(self, board):
        selection = self.possibilities(board)
        return random.choice(selection)
    
    def possibilities(self, board):
        l = []

        for i in range(len(board)):
            for j in range(len(board)):

                if board[i][j] == 0:
                    l.append((i, j))
        return (l)
        
    def bad_action(self):
        return 0


class Human(Player):
    def __init__(self, indicator):
        self.indicator = indicator
        self.action = ()

    def choose_action(self, board):
        selection = self.possibilities(board)
        while self.action not in selection:
            action_raw = input("make a choice, type x,y: ").split(',')
            self.action = tuple(int(cordinate) for cordinate in action_raw)
            print(self.action in selection)
        return self.action


class Agent(Player):
    def __init__(self, indicator, gamma, debug=False):
        self.gamma = gamma
        self.indicator = indicator
        self.statesFound = 0
        self.debug = debug
        self.qTable = np.zeros(shape=[19668, 9])
        self.stateIndexMap = {}
        self.epsilon = 0.1
        self.moves = []
        self.max_epsilon = 1.0
        self.min_epsilon = 0.01
        self.decay_rate = 0.01
        self.allActions = [(0, 0), (0, 1), (0, 2),
                           (1, 0), (1, 1), (1, 2),
                           (2, 0), (2, 1), (2, 2)]

    # returns an action
    def choose_action(self, board):
        chosenAction = ()
        actionIndex = 99
        stateIndex = self.stateIndexMap[self._hashBoardState(board)]
        if random.uniform(0, 1) < self.epsilon:
            # random from available actions
            chosenAction = random.choice(self.possibilities(board))
            actionIndex = self.allActions.index(chosenAction)
        else:
            # action from Q-table
            actionIndex = np.argmax(self.qTable[stateIndex])
            chosenAction = self.allActions[actionIndex]

        self.epsilon = self.min_epsilon + \
            (self.max_epsilon-self.min_epsilon) * np.exp(-0.1*self.epsilon)
        
        self.moves.append((stateIndex, actionIndex))
        if self.debug:
            print('Agent chosen action: ', chosenAction)
        return chosenAction
    
    def bad_action(self):
        lastMove = self.moves.pop()
        self.qTable[lastMove[0]][lastMove[1]] = -1

    def _normalizeIndicators(self, x):
        return x if (x == 0 or x == self.indicator) else 9

    def _setNewState(self, stateHash):
        self.stateIndexMap[stateHash] = self.statesFound
        self.statesFound +=1

    def _hashBoardState(self, state):
        normalizedState = [self._normalizeIndicators(x) for x in state.flatten().tolist()]
        stateHash = ''.join(str(i) for i in normalizedState)
        
        if stateHash not in self.stateIndexMap:
            self._setNewState(stateHash)
        
        return stateHash

            


    # def measureReward(self, action, state):
    #     return 0

    # def updateQ(self, action, state):
    #     return 0

    # def mapQvalueToAction(self, state)
