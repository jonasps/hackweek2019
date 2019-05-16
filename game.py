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
def play_game(player1, player2):
    board, winner, counter = create_board(), 0, 1
    while winner == 0:
        print(board)
        for player in [player1, player2]:
            action = player.choose_action(board)
            # handle choosen action
            print('counter: ', counter)
            while action not in possibilities(board):
                player.bad_action()
                print(player.choose_action(board))
                action = player.choose_action(board)

            board[action] = player.indicator
            counter += 1
            winner = evaluate(board, [player1, player2])
            if winner != 0:
                print(board)
                break
    return (winner)


# Driver Code
human = Human(8)
agent = Agent(0, 3, True)
print("Winner is: " + str(play_game(human, agent)))
