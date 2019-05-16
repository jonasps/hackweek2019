import numpy as np
import random

def class Agent:

    def __init (self, gamma, char):
        self.gamma = gamma
        self.player = char
        self.qTable = np.matrix([8, 8])
        self.epsilon = 0.1
        self.max_epsilon=1.0
        self.min_epsilon=0.01
        self.decay_rate = 0.01

    #returns an action 
    def chooseAction(self, availableActions):
        if random.uniform(0,1) < self.epsilon:
            #random from available actions
            return random.choice(availableActions)
        else:
            #action from Q-table
            return np.argmax(qTable[state])

    def measureReward(action, state):

    def updateQ(action state):
        
