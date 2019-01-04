import random
from Board import Board
from solver.Solver import Solver

class User(object):
    def __init__(self):
        self.x = ''

if __name__ == '__main__':
    width = 24
    height = 24
    mines = 99
    board = Board()
    board.init_board(width, height, mines)
    board.print_game_board()
    solver = Solver()
    if solver.solve_minesweeper(board):
        print("SUCCESS")
    else:
        print("FAIL!!!")
