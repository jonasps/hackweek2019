# Tic-Tac-Toe Program using
# random number in Python

# importing all necessary libraries
import numpy as np
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
                    print('winning boardState: \n', board)
                if winner == player1.indicator:
                    player1.end_game_evaluation(100)
                    player1.wins += 1
                    player2.end_game_evaluation(-100)
                elif winner == player2.indicator:
                    player1.end_game_evaluation(-100)
                    player2.end_game_evaluation(100)
                    player2.wins += 1
                else:
                    player1.end_game_evaluation(0)
                    player2.end_game_evaluation(0)
                    player1.draws += 1
                    player2.draws += 1
                break
    return (winner)

def train(iterations, player1, player2):
    player1.debug = False
    player2.debug = False
    for i in range(30000):
        play_game(player1, player2, True)
        play_game(player2, player1, True)
        if i % 1000 == 0:
            print(i)
            print('agent1 wins: ' + str(player1.wins),
                'agent2 wins: ' + str(player2.wins))
            print('draws ' + str(player1.draws))
    player1.debug = True
    player2.debug = True
    if player1.wins > player2.wins:
        player1.wins = 0
        player1.draws = 0
        player1.save_qtable()
        return player1
    else:
        player2.wins = 0
        player2.draws = 0
        player2.save_qtable()
        return player2

def test_agent(agent):
    human = Human(8)
    agent.debug = True
    for i in range(700):
        print("Winner is: " + str(play_game(agent, human, False)))
        print("Winner is: " + str(play_game(human, agent, False)))

# Driver Code
best_so_far = Agent(2, 0, 1, False)
best_so_far.load_qtable('best_so_far')
test_agent(best_so_far)
agent = Agent(1, 0.6, 0.4, False)
agent2 = Agent(2, 0.7, 0.2, False)
agent3 = Agent(3, 0.8, 0.3, False)
agent4 = Agent(4, 0.9, 0.1, False)
winner1 = train(10000, agent, agent2)
winner2 = train(10000, agent3, agent4)
winner3 = train(10000, winner1, winner2)
winner3.set_epsilon(1)
winner3.set_epsilon(1)
for i in range(700):
    print("Winner is: " + str(play_game(winner3, human, False)))
    print("Winner is: " + str(play_game(human, winner3, False)))

