import numpy as np
import random
import hashlib
import pickle

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
    def __init__(self, indicator, learning_rate, epsilon, debug=False):
        self.learning_rate = learning_rate
        self.min_learning_rate = 0.1
        self.indicator = indicator
        self.opponent_indicator = 9
        self.state_observations = 0
        self.action_space = [(0, 0), (0, 1), (0, 2),
                           (1, 0), (1, 1), (1, 2),
                           (2, 0), (2, 1), (2, 2)]
        self.debug = debug
        self.qTable = np.zeros(shape=[self.state_observations , len(self.action_space)])
        self.stateIndexMap = {}
        self.moves = []
        self.decay_rate = 0.9999
        self.discount_factor = 0.8
        self.wins = 0
        self.draws = 0
        self.epsilon = epsilon
        self.min_epsilon = 0.1
        self.epsilonHistory = []


    def _future_simulated_reward(self, action, board):
        future_board = np.array(board, copy=True)

        if future_board[action] == 0:
            # we make our action
            future_board[action] = self.indicator

            # we make our opponents predicted action (based on our knowledge)
            opponent_action = self._opponent_action_prediction(future_board)
            if not opponent_action:
                return 0

            future_board[opponent_action] = self.opponent_indicator
            
            # our future predicted next state 
            futureHash = self._hash_array(future_board)
            if futureHash in self.stateIndexMap:

                # we find our biggest q-value in our future state
                stateIndex = self.stateIndexMap[futureHash]
                qList = self.qTable[stateIndex].tolist()

                return np.amax(qList)
        return 0

    
    def _opponent_action_prediction(self, board):
        chosenAction = ()
        opponentHash = self._hash_array(board, True)
        
        if opponentHash in self.stateIndexMap:
            stateIndex = self.stateIndexMap[opponentHash]

            # action from Q-table
            qList = self.qTable[stateIndex].tolist()
            action_candidates = np.argwhere(qList == np.amax(qList)).flatten()

            actionIndex = random.choice(action_candidates)
            chosenAction = self.action_space[actionIndex]
        else:
            if len(self.possibilities(board)) == 0:
                return False

            chosenAction = random.choice(self.possibilities(board))

        if self.debug:
            print('Simulated oppunent action: ', chosenAction)
        return chosenAction

    # returns an action
    def choose_action(self, board):
        chosenAction = ()
        actionIndex = 99

        stateIndex = self.stateIndexMap[self._process_board_state(board)]
        if  random.random() > self.epsilon:
            # action from Q-table
            qList = self.qTable[stateIndex].tolist()
            action_candidates = np.argwhere(qList == np.amax(qList)).flatten()
            
            for a in action_candidates:
                self._future_simulated_reward(
                    self.action_space[a], board)
            
            if self.debug:
                print('exploit')
                print('available Q-values for state: ', self.qTable[stateIndex])
                print('action candidates: ', action_candidates)
            actionIndex = random.choice(action_candidates)
            chosenAction = self.action_space[actionIndex]
        else:
            if self.debug:
                print('explore, epsilon: ', self.epsilon)
            # random from available actions
            chosenAction = random.choice(self.possibilities(board))
            actionIndex = self.action_space.index(chosenAction)  
        
        self.moves.append((stateIndex, actionIndex))
        if self.debug:
            print('Agent chosen action: ', chosenAction)
        return chosenAction    

    def save_agent(self, file_name=''):
        if not file_name:
            file_name = str(self.indicator)
       
        np.savetxt('qtable-{}.csv'.format(file_name), np.around(np.column_stack(
            self.qTable), decimals=5), fmt='%.2f', delimiter=',')
        
        with open('index-map-{}.pkl'.format(file_name), 'wb') as f:
            pickle.dump(self.stateIndexMap, f, pickle.HIGHEST_PROTOCOL)

    def load_agent(self, indicator):
        self.qTable = np.loadtxt('qtable-{}.csv'.format(
            indicator), delimiter=',').transpose()
        self.state_observations = len(self.qTable)

        with open('index-map-{}.pkl'.format(indicator), 'rb') as f:
            self.stateIndexMap = pickle.load(f)

    def bad_action(self):
        lastMove = self.moves.pop()
        self.qTable[lastMove[0]][lastMove[1]] = self.q_value_for(lastMove) - 1000
        if self.debug:
            print('agent bad move: ', self.action_space[lastMove[1]])
    
    def end_game_evaluation(self, reward):        
        rewardedMove = self.moves.pop()
        self.qTable[rewardedMove[0]][rewardedMove[1]] = self.q_value_for(rewardedMove) + reward

        while len(self.moves) > 0:
            reward *= self.discount_factor
            previousMove = self.moves.pop()
            self.qTable[previousMove[0]][previousMove[1]] = self.q_value_for(previousMove) + (reward * self.discount_factor)
            #if self.learning_rate > self.min_learning_rate:
            #    self.learning_rate *= self.decay_rate
            if self.epsilon > self.min_epsilon:
                self.epsilon *= self.decay_rate
                self.epsilonHistory.append(self.epsilon)

    def q_value_for(self, move):
        return self.qTable[move[0]][move[1]]

    def _normalizeIndicators(self, x, indicator, opponent_indicator):
        if x == 0:
            return x
        elif x == indicator:
             return -1
        else:
            return opponent_indicator

    def _setNewState(self, stateHash):
        self.stateIndexMap[stateHash] = self.state_observations
        new_row = np.zeros(shape = [1, len(self.action_space)])
        # print('q-table actions: \n', len(self.qTable[0]))
        # print('new row actions: \n', len(new_row[0]))
        self.qTable = np.append(self.qTable, new_row, axis=0)
        self.state_observations +=1

    def _hash_array(self, board, opponentHash=False):
        indicator = self.indicator
        opponent_indicator = self.opponent_indicator

        if opponentHash:
            indicator = self.opponent_indicator
            opponent_indicator = self.indicator

        normalizedState = [self._normalizeIndicators(
            x, indicator, opponent_indicator) for x in board.flatten().tolist()]
        stateHash = ''.join(str(i) for i in normalizedState)

        return stateHash

    def _process_board_state(self, board):
        stateHash = self._hash_array(board)
        
        if stateHash not in self.stateIndexMap:
            self._setNewState(stateHash)
        
        return stateHash
