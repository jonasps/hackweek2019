import numpy as np
import random

class Agent:

    def __init (self, indicator, gamma, char):
        self.gamma = gamma
        self.indicator = indicator
        self.player_type = "agent"
        self.qTable = np.matrix([8, 8])
        self.epsilon = 0.1
        self.max_epsilon=1.0
        self.min_epsilon=0.01
        self.decay_rate = 0.01

    #returns an action 
    def chooseAction(self, availableActions, state):
        if random.uniform(0,1) < self.epsilon:
            #random from available actions
            return random.choice(availableActions)
        else:
            #action from Q-table
            return np.argmax(self.qTable[state])

    def measureReward(self, action, state):
        return 0

    def updateQ(self, action, state):
        return 0
        
