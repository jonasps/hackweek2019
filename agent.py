import numpy as np
import random


class Agent:

    def __init(self, indicator, gamma, indicator, debug=False):
        self.gamma = gamma
        self.indicator = indicator
        self.qTable = np.matrix(np.zeros(shape=[9, 3]))
        self.epsilon = 0.1
        self.max_epsilon = 1.0
        self.min_epsilon = 0.01
        self.decay_rate = 0.01
        self.allActions = np.array([[0, 0], [0, 1], [0, 2],
                           [1, 0], [1, 1], [1, 2],
                           [2, 0], [2, 1], [2, 2]])

    # returns an action
    def chooseAction(self, availableActions, state):
        if random.uniform(0, 1) < self.epsilon:
            # random from available actions
            return random.choice(availableActions)
        else:
            # action from Q-table
            np.argmax(self.qTable[state])
            # [0,0,0,0,0,0,0,0,0]
            return
        self.epsilon = self.min_epsilon + \
            (self.max_epsilon-self.min_epsilon) * np.exp(-0.1*self.epsilon)

    def measureReward(self, action, state):
        return 0

    def updateQ(self, action, state):
        return 0

    def mapQvalueToAction(self, state)
