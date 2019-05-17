# Tic-Tac-Toe Program using
# random number in Python

# importing all necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import random

from agent import Agent, Player, Human

# Creates an empty board


def create_board():
    return (np.array([[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]))


# Check for empty places on board
def possibilities(board):
    l = []

    for i in range(len(board)):
        for j in range(len(board)):

            if board[i][j] == 0:
                l.append((i, j))
    return (l)


def row_win(board, playerIndicator):
    for x in range(len(board)):
        win = True

        for y in range(len(board)):
            if board[x, y] != playerIndicator:
                win = False
                continue

        if win == True:
            return (win)
    return (win)


# Checks whether the player has three
# of their marks in a vertical row
def col_win(board, playerIndicator):
    for x in range(len(board)):
        win = True

        for y in range(len(board)):
            if board[y][x] != playerIndicator:
                win = False
                continue

        if win == True:
            return (win)
    return (win)


# Checks whether the player has three
# of their marks in a diagonal row
def diag_win(board, playerIndicator):
    win = True

    for x in range(len(board)):
        if board[x, x] != playerIndicator:
            win = False
    
    if win == True:
        # left to right
        return (win)
    
    win = True
    for x in range(len(board)):
        if board[x, (2 - x)] != playerIndicator:
            win = False
    
    return (win)


# Evaluates whether there is
# a winner or a tie
def evaluate(board, playerlist):
    winner = 0

    for player in playerlist:
        if (row_win(board, player.indicator) or
                col_win(board, player.indicator) or
                diag_win(board, player.indicator)):
            # return winner
            winner = player.indicator

    if np.all(board != 0) and winner == 0:
        winner = -1
    return winner


# Main function to start the game
def play_game(player1, player2, training):
    board, winner, counter = create_board(), 0, 1
    while winner == 0:
        for player in [player1, player2]:
            if not training:
                print('current board state: \n', board)
            action = player.choose_action(board)
            # handle choosen action
            #print('counter: ', counter)
            while action not in possibilities(board):
                if action == "quit":
                    return -1
                player.bad_action()
                action = player.choose_action(board)

            board[action] = player.indicator
            counter += 1
            winner = evaluate(board, [player1, player2])
            if winner != 0:
                if not training:
                    print('last boardState: \n', board)
                if winner == player1.indicator:
                    player1.end_game_evaluation(100)
                    player1.wins += 1
                    player2.end_game_evaluation(-100)
                elif winner == player2.indicator:
                    player1.end_game_evaluation(-100)
                    player2.end_game_evaluation(100)
                    player2.wins += 1
                else:
                    player1.end_game_evaluation(1)
                    player2.end_game_evaluation(1)
                    player1.draws += 1
                    player2.draws += 1
                break
    return 'player{} won the game!'.format(winner) if winner > 0 else 'Game is a tie!'

def train(iterations, player1, player2):
    player1.debug = False
    player2.debug = False
    for i in range(iterations):
        play_game(player1, player2, True)
        play_game(player2, player1, True)
        if i % 1000 == 0:
            print(i)
            print('agent{} wins: {}'.format(player1.indicator, str(player1.wins)),
                  'agent{} wins: {}'.format(player2.indicator, str(player2.wins)))
            print('draws {}'.format(str(player1.draws)))
    player1.debug = True
    player2.debug = True
    if player1.wins > player2.wins:
        player1.wins = 0
        player1.draws = 0
        player1.save_agent()
        return player1
    else:
        player2.wins = 0
        player2.draws = 0
        player2.save_agent()
        return player2

def test_agent(agent):
    human = Human(8)
    agent.debug = True
    agent.epsilon = 0
    for i in range(700):
        print(play_game(human, agent, False))
        print(play_game(agent, human, False))

# Driver Code
best_so_far = Agent(10, 0, 1, False)
best_so_far.load_agent(10)
test_agent(best_so_far)

agent = Agent(1, 0.6, 1)
agent2 = Agent(2, 0.7, 1)
agent3 = Agent(3, 0.8, 1)
agent4 = Agent(4, 0.9, 1)
agent10 = Agent(10, 0.7, 1)
agent11 = Agent(11, 0.8, 1)
agent12 = Agent(12, 0.9, 1)
agent13 = Agent(13, 1, 1)
semi1 = train(5000, agent, agent2)
semi2 = train(5000, agent3, agent4)
semi3 = train(5000, agent10, agent11)
semi4 = train(5000, agent12, agent13)
finalist1 = train(10000, semi1, semi2)
finalist2 = train(10000, semi3, semi4)
winner = train(50000, finalist1, finalist2)
plt.plot(winner.epsilonHistory)
print('epsilon len: ', len(winner.epsilonHistory))
plt.ylabel('epsilon value')
plt.show()

test_agent(winner)
