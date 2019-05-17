import numpy as np
import random
import hashlib

# Check for empty places on board


class Player:
    def __init__(self, indicator):
        self.indicator = indicator
        self.wins = 0
        self.draws = 0

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
    
    def end_game_evaluation(self, reward):
        return 0


class Human(Player):
    def __init__(self, indicator):
        self.indicator = indicator
        self.action = ()
        self.wins = 0
        self.draws = 0

    def choose_action(self, board):
        #selection = self.possibilities(board)
        #while self.action not in selection:
        action_raw = input("make a choice, type x,y: ").split(',')
        if action_raw == "q":
            return "quit"
        self.action = tuple(int(cordinate) for cordinate in action_raw)
        return self.action


class Agent(Player):
    def __init__(self, indicator, gamma, epsilon, debug=False):
        self.gamma = gamma
        self.indicator = indicator
        self.statesFound = 0
        self.debug = debug
        self.qTable = np.zeros(shape=[19668, 9])
        self.stateIndexMap = {}
        self.epsilon = epsilon
        self.moves = []
        self.max_epsilon = 0.85
        self.min_epsilon = 0.01
        self.decay_rate = 0.01
        self.discount_factor = 0.01
        self.wins = 0
        self.draws = 0
        self.allActions = [(0, 0), (0, 1), (0, 2),
                           (1, 0), (1, 1), (1, 2),
                           (2, 0), (2, 1), (2, 2)]

    # returns an action
    def choose_action(self, board):
        chosenAction = ()
        actionIndex = 99
        stateIndex = self.stateIndexMap[self._hashBoardState(board)]
        if  random.random() < self.epsilon:
            # action from Q-table
            if self.debug:
                print('exploit')
                print('available Q-values for state: ', self.qTable[stateIndex])
                print('actionIndex: ', np.argmax(self.qTable[stateIndex]))
            actionIndex = np.argmax(self.qTable[stateIndex])
            chosenAction = self.allActions[actionIndex]
        else:
            if self.debug:
                print('explore, epsilon: ', self.epsilon)
            # random from available actions
            chosenAction = random.choice(self.possibilities(board))
            actionIndex = self.allActions.index(chosenAction)
            
        #self.epsilon = self.min_epsilon + \
        #    (self.max_epsilon-self.min_epsilon) * np.exp(-0.1*self.epsilon)
        if self.epsilon < self.max_epsilon:
            self.epsilon += self.decay_rate            
        
        self.moves.append((stateIndex, actionIndex))
        if self.debug:
            print('Agent chosen action: ', chosenAction)
        return chosenAction
    

    def save_qtable(self):
        np.savetxt('{}.csv'.format(self.indicator), np.around(np.column_stack(
            self.qTable), decimals=5), fmt='%.2f', delimiter=',')

    def load_qtable(self, indicator):
        self.qTable = np.loadtxt('{}.csv'.format(indicator), delimiter=',')

    def bad_action(self):
        lastMove = self.moves.pop()
        self.qTable[lastMove[0]][lastMove[1]] = self.q_value_for(lastMove) - 1000
        if self.debug:
            print('agent bad move: ', lastMove)
            print('updated q values for state: ', self.qTable[lastMove[0]])
    
    def end_game_evaluation(self, reward):
        if self.debug:
            print('------- end game eval -------------- \n', len(self.moves), self.moves)
        
        while len(self.moves) > 0:
            previousMove = self.moves.pop()
            self.qTable[previousMove[0]][previousMove[1]] = self.q_value_for(previousMove) + (reward * self.discount_factor)
            reward = self.discount_factor * reward

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def q_value_for(self, move):
        return self.qTable[move[0]][move[1]]

    def _normalizeIndicators(self, x):
        if x == 0:
            return x
        elif x == self.indicator:
             return 1
        else:
            return 9

    def _setNewState(self, stateHash):
        #if self.debug:
        #print('new state found: ', stateHash)
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
