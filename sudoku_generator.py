import pygame
import sys
import math
import random

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


class SudokuGenerator:
    '''
    create a sudoku board - initialize class variables and set up the 2D board
    This should initialize:
    self.row_length       - the length of each row
    self.removed_cells - the total number of cells to be removed
    self.board       - a 2D list of ints to represent the board
    self.box_length       - the square root of row_length

    Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

    Return:
    None
    '''

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = int(math.sqrt(row_length))
        self.board = []
        for i in range(row_length):
            row = [0] * row_length
            self.board.append(row)
        return None

    '''
    Returns a 2D python list of numbers which represents the board

    Parameters: None
    Return: list[list]
    '''

    def get_board(self):
        return self.board

    '''
    Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

    Parameters: None
    Return: None
    '''

    def print_board(self):
        for row in self.board:
            print(" ".join(map(str, row)))

    '''
    Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

    Parameters:
    row is the index of the row we are checking
    num is the value we are looking for in the row

    Return: boolean
    '''

    def valid_in_row(self, row, num):
        found = True
        for i in range(self.row_length):
            if num == self.board[row][i]:
                found = False
                break
        return found

    '''
    Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

    Parameters:
    col is the index of the column we are checking
    num is the value we are looking for in the column

    Return: boolean
    '''

    def valid_in_col(self, col, num):
        found = True
        for i in range(self.row_length):
            if num == self.board[i][col]:
                found = False
                break
        return found

    '''
    Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

    Parameters:
    row_start and col_start are the starting indices of the box to check
    i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
    num is the value we are looking for in the box

    Return: boolean
    '''

    def valid_in_box(self, row_start, col_start, num):
        found = True
        for i in range(3):
            for j in range(3):
                if num == self.board[row_start + i][col_start + j]:
                    found = False
                    break
        return found

    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

    Parameters:
    row and col are the row index and col index of the cell to check in the board
    num is the value to test if it is safe to enter in this cell

    Return: boolean
    '''

    def is_valid(self, row, col, num):
        valid_row = row // 3 * 3
        valid_col = col // 3 * 3
        return self.valid_in_row(row, num) and self.valid_in_col(col, num) and self.valid_in_box(valid_row, valid_col,num)

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

    Parameters:
    row_start and col_start are the starting indices of the box to check
    i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

    Return: None
    '''

    def fill_box(self, row_start, col_start):
        for i in range(3):
            for j in range(3):
                while True:
                    filled_box = random.randint(1, 9)
                    if self.valid_in_box(row_start, col_start, filled_box):
                        self.board[row_start + i][col_start + j] = filled_box
                        break

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

    Parameters: None
    Return: None
    '''

    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

    Parameters:
    row, col specify the coordinates of the first empty (0) cell

    Return:
    boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def get_row_length(self):
        return self.row_length

    def get_removed_cells(self):
        return self.removed_cells

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

    Parameters: None
    Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called

    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

    Parameters: None
    Return: None
    '''

    def remove_cells(self):
        remove_cells = self.removed_cells
        total_cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(total_cells)
        for i in range(remove_cells):
            row, col = total_cells[i]
            self.get_board()[row][col] = 0
        return None

    '''
    DO NOT CHANGE
    Provided for students
    Given a number of rows and number of cells to remove, this function:
    1. creates a SudokuGenerator
    2. fills its values and saves this as the solved state
    3. removes the appropriate number of cells
    4. returns the representative 2D Python Lists of the board and solution

    Parameters:
    size is the number of rows/columns of the board (9 for this project)
    removed is the number of cells to clear (set to 0)

    Return: list[list] (a 2D Python list to represent the board)
    '''


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row_index = row
        self.col_index = col
        self.screen = screen
        self.isSelected = False
        self.selected = False
        self.sketched_value = None
        # self.width = width
        self.filled = False
        self.black_color = (0, 0, 0)
        self.light_gray_color = (200, 180, 200)
        self.red_color = (255, 0, 0)
        self.white_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 36)


    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def set_selected(self, selected):
        self.isSelected = selected

    def draw(self):
        cell_size = self.screen.get_width() // 9
        x_pos = self.col_index * cell_size
        y_pos = self.row_index * cell_size

        # Draw the cell
        pygame.draw.rect(self.screen, self.white_color, (x_pos, y_pos, cell_size, cell_size))
        border_color_cell = self.red_color if self.isSelected else self.black_color
        pygame.draw.rect(self.screen, border_color_cell, (x_pos, y_pos, cell_size, cell_size), 1)

        # Black border around 3x3 boxes
        if self.col_index % 3 == 2 and self.col_index < 8:
            pygame.draw.line(self.screen, self.black_color, (x_pos + cell_size, y_pos),
                             (x_pos + cell_size, y_pos + cell_size), 8)
        if self.row_index % 3 == 2 and self.row_index < 8:
            pygame.draw.line(self.screen, self.black_color, (x_pos, y_pos + cell_size),
                             (x_pos + cell_size, y_pos + cell_size), 8)

        # User sketched values will become gray and once filled will become black
        text_value_cell = str(self.value) if self.value != 0 else ''
        text_color_filled = self.black_color if self.value != 0 and self.sketched_value is None else self.light_gray_color
        text_surface_filled = self.font.render(text_value_cell, True, text_color_filled)
        text_rect_filled = text_surface_filled.get_rect(
            center=(x_pos + cell_size // 2, y_pos + cell_size // 2))
        self.screen.blit(text_surface_filled, text_rect_filled)


class Board:
    def __init__(self, width, height, screen, difficulty):
        prog_levels = {"easy": 30, "medium": 40, "hard": 50}
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cell_size = width // 9
        self.black = (0, 0, 0)
        self.rows = 9
        self.cols = 9
        self.selected_row = None
        self.selected_col = None
        xboard = generate_sudoku(9, prog_levels[difficulty])
        self.board = xboard
        self.org_board = [row[:] for row in xboard]
        self.cells = [
            [Cell(self.board[i][j], i, j, screen) for j in range(self.cols)]
            for i in range(self.rows)
        ]

    def draw(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw()
        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(self.screen, self.black, (i * self.cell_size, 0), (i * self.cell_size, self.height), 4)
                pygame.draw.line(self.screen, self.black, (0, i * self.cell_size), (self.width, i * self.cell_size), 4)
            else:
                pygame.draw.line(self.screen, self.black, (i * self.cell_size, 0), (i * self.cell_size, self.height), 2)
                pygame.draw.line(self.screen, self.black, (0, i * self.cell_size), (self.width, i * self.cell_size), 2)

    def select(self, row, col):
        rrr = (255, 0, 0)
        self.selected_row = row
        self.selected_col = col
        pygame.draw.rect(self.screen, rrr, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size),3)


    def click(self, x, y):
        row, col = y // self.cell_size, x // self.cell_size
        # print(x,y)
        if (0 <= row < 9) and (0 <= col < 9):
            return (row, col)
        else:
            return (None, None)

    def clear(self):
        if self.org_board[self.selected_row][self.selected_col] == 0:
            self.board[self.selected_row][self.selected_col] = 0
            self.update_cells()

    def sketch(self, value):
        row = self.selected_row
        col = self.selected_col
        if row is not None:
            self.board[row][col] = value
            self.update_cells()

    def update_cells(self):
        self.cells = [
            [Cell(self.board[i][j], i, j, self.screen) for j in range(self.cols)]
            for i in range(self.rows)
        ]
        for i in range(self.rows):
            for j in range(self.cols):
                if self.org_board[i][j] == 0 and self.board[i][j] != 0:
                    self.cells[i][j].set_cell_value(self.board[i][j])
                    self.cells[i][j].set_sketched_value(self.board[i][j])

    def place_number(self, value):
        if self.selected_row is not None and self.selected_col is not None:
            cell = self.cells[self.selected_row][self.selected_col]
            cell.filled = True
            cell.sketched_value = False
            cell.set_cell_value(value)
            self.update_cells()

    def reset_to_original(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = self.org_board[i][j]
        self.update_cells()

    def is_full(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    return False
        return True

    def update_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = self.cells[i][j].value

    def find_empty(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def check_board(self):
        for i in range(self.rows):
            if not self.valid_values(self.board[i]):
                return False
        for j in range(self.cols):
            col_vals = [self.board[i][j] for i in range(self.rows)]
            if not self.valid_values(col_vals):
                return False
        for i in range(0, self.rows, 3):
            for j in range(0, self.cols, 3):
                grid_vals = [
                    self.board[row][col]
                    for row in range(i, i + 3)
                    for col in range(j, j + 3)
                ]
                if not self.valid_values(grid_vals):
                    return False
        return True

    def valid_values(self, values):
        duplicate_value = set()
        for value in values:
            if value != 0:
                if value in duplicate_value:
                    return False
                duplicate_value.add(value)
        return True

