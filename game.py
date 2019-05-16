# Tic-Tac-Toe Program using
# random number in Python

# importing all necessary libraries
import numpy as np
import random

# Creates an empty board


class Player:
    def __init__(self, indicator, player_type='random'):
        self.player_type = player_type
        self.indicator = indicator

    # Select a random place for the player

    def choose_action(self, board):
        selection = possibilities(board)
        return random.choice(selection)


class Human(Player):
    def __init__(self, indicator, player_type='human'):
        self.player_type = player_type
        self.indicator = indicator
        self.action = ()

    def choose_action(self, board):
        selection = possibilities(board)
        while self.action not in selection:
            action_raw = input("make a choice, type x,y: ").split(',')
            self.action = tuple(int(cordinate) for cordinate in action_raw)
            print(self.action in selection)
        return self.action


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
def play_game(player1=Player(1), player2=Player(2)):
    board, winner, counter = create_board(), 0, 1
    while winner == 0:
        print(board)
        for player in [player1, player2]:
            action = player.choose_action(board)
            board[action] = player.indicator
            counter += 1
            winner = evaluate(board, [player1, player2])
            if winner != 0:
                break
    return (winner)


# Driver Code
human = Human(8)
print("Winner is: " + str(play_game(human, Player(1))))
