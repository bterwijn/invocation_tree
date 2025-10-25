import itertools as it

class Sudoku:
    def __init__(self, board_string):
        self.board = self.parse_board(board_string)
        self.open_positions = self.get_open_positions()

    def parse_board(self, board_string):
        board = []
        for line in it.batched(board_string, 9):
            row = [int(char) for char in line]
            board.append(row)
        return board

    def get_open_positions(self):
        open_positions = set()
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    open_positions.add((r, c))
        return open_positions

    def get_valid_values(self, row, col):
        valid_values = {i for i in range(1, 10)}
        # Check row
        for c in range(9):
            if self.board[row][c] != 0:
                valid_values.discard(self.board[row][c])
        # Check column
        for r in range(9):
            if self.board[r][col] != 0:
                valid_values.discard(self.board[r][col])
        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] != 0:
                    valid_values.discard(self.board[r][c])
        return valid_values

    def set_position(self, row, col, value):
        self.board[row][col] = value
        self.open_positions.discard((row, col))

    def unset_position(self, row, col):
        self.board[row][col] = 0
        self.open_positions.add((row, col))

    def __repr__(self):
        return "\n" + "\n".join(" ".join(str(num) if num != 0 else '.' for num in row) for row in self.board)

def solve_sudoku(sudoku):
    if not sudoku.open_positions:
        return True  # Solved

    # see which open position there are and what valid values they have
    open_positions = list(sudoku.get_open_positions())
    positions_valid_values = []
    for r,c in open_positions:
        positions_valid_values.append(sudoku.get_valid_values(r, c))

    # pick the open position with the fewest valid values
    min_index = min(range(len(positions_valid_values)), key=lambda i: len(positions_valid_values[i]))
    
    row, col = open_positions[min_index]
    valid_values = positions_valid_values[min_index]

    # clean up
    del open_positions, positions_valid_values, min_index, r, c 

    # try each valid value for that position
    for value in valid_values:
        sudoku.set_position(row, col, value)
        if solve_sudoku(sudoku):
            return True
        sudoku.unset_position(row, col)

    return False  # Trigger backtracking


# from https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/
easy = "050703060007000800000816000000030000005000100730040086906000204840572093000409000"
medium = "020900000048000031000063020009407003003080200400105600030570000250000180000006050"
hard = "080200400570000100002300000820090005000715000700020041000006700003000018007009050"
diabolical = "083020090000800100029300008000098700070000060006740000300006980002005000010030540"

sudoku = Sudoku(hard)
print("start state:", sudoku)

ivt_tree.max_string_len = 200
ivt_tree.ignore_calls.add('Sudoku.get_open_positions')
ivt_tree.ignore_calls.add('Sudoku.get_valid_values')
ivt_tree.ignore_calls.add('Sudoku.set_position')
ivt_tree.ignore_calls.add('<lambda>')

solve_sudoku(sudoku)
print('final state:', sudoku)
