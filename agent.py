import numpy as np
import random
import hashlib


class Agent:

    def __init(self, indicator, gamma, indicator, debug=False):
        self.gamma = gamma
        self.indicator = indicator
        self.statesFound = 0
        self.qTable = np.matrix(np.zeros(shape=[19668, 9]))
        self.stateIndexMap = {}
        self.epsilon = 0.1
        self.max_epsilon = 1.0
        self.min_epsilon = 0.01
        self.decay_rate = 0.01
        self.allActions = np.array([[0, 0], [0, 1], [0, 2],
                                    [1, 0], [1, 1], [1, 2],
                                    [2, 0], [2, 1], [2, 2]])

    # returns an action
    def chooseAction(self, availableActions, state):
        bestAction = ()
        if random.uniform(0, 1) < self.epsilon:
            # random from available actions
            bestAction = random.choice(availableActions)
        else:
            # action from Q-table
            stateHash = hashBoardState(state)
            qActionIndex = np.argmax(self.qTable[self.stateIndexMap[stateHash]])
            bestAction = self.allActions[qActionIndex]

        self.epsilon = self.min_epsilon + \
            (self.max_epsilon-self.min_epsilon) * np.exp(-0.1*self.epsilon)
        
        return bestAction

    def _normalizeIndicators(self, x):
        return x if (x == 0 or x == self.indicator) else 9

    def _setNewState(self, stateHash):
        self.stateIndexMap[stateHash] = self.statesFound
        self.statesFound +=1

    def hashBoardState(self, state):
        normalizedState = [_normalizeIndicators(
            x) for x in state.flatten().tolist()]
        stateHash = ''.join(str(i) for i in normalizedState)
        
        if stateHash not in self.stateIndexMap:
            _setNewState(stateHash)
        
        return stateHash
            


    def measureReward(self, action, state):
        return 0

    def updateQ(self, action, state):
        return 0

    def mapQvalueToAction(self, state)
