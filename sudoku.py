# author: ali jandaghian
# Sudoku Solver

def get_grids(puzzle_grid):
    """Converts list of sudoku numbers (81 numbers) to following:
        - list of 9 rows, each row contains 9 numbers (it represents rows of sudoku puzzle).
        - list of 9 columns, each row contains 9 number (it represents columns of sudoku puzzle).
        - list of 9 sub squares, each sub list contains 9 numbers (it represents 3x3 squares).
    :param puzzle_grid: list of 81 numbers of a sudoku puzzle (list of integers)
    :return: tuple of list of rows, list of columns, and list of sub 3x3 squares.
    """
    # split puzzle numbers into sub lists of 9 numbers (a row) to make list of rows of a sudoku
    puzzle_grid_row = [puzzle_grid[index:index + 9] for index in range(0, 81, 9)]

    # assume puzzle list (81 numbers) is in 9x9 square, code below picks every 9 numbers in a column into a sub list.
    puzzle_grid_col = [[puzzle_grid[i + j * 9] for j in range(9)] for i in range(9)]

    # assume puzzle list in 9 3x3 squares, code below picks every 9 numbers in a 3x3 squares into a sub list.
    puzzle_grid_sub = [[puzzle_grid[i // 3 * 27 + (i % 3) * 3 + j // 3 * 9 + j % 3] for j in range(9)] for i in
                       range(9)]
    return puzzle_grid_row, puzzle_grid_col, puzzle_grid_sub


def find_coordinates(index):
    """Finds row, column, and sub square index for a given index (0 to 80). All row, column and sub 3x3 square
    indexes are integer between 0 and 8, including both 0 and 8. for exapmle, for the indicated cell in puzzle grid
    below, index is 13 therefore the row index is 1, column index is 4, and sub square index is 1.

            column indexes:   0  1  2   3  4  5   6  7  8

      row indexes:            ---0---   ---1---   ---2---
                   0          0  0  4   0  0  6   0  7  9
                   1          0  0  0   0 [0] 0   6  0  2
                   2          0  5  6   0  9  2   3  0  0

                              ---3---   ---4---   ---5---                    sub 3x3 square indexes: ---x---
                   3          0  7  8   0  6  1   0  3  0
                   4          5  0  9   0  0  0   4  0  6
                   5          0  2  0   5  4  0   8  9  0

                              ---6---   ---7---   ---8---
                   6          0  0  7   4  1  0   9  2  0
                   7          1  0  5   0  0  0   0  0  0
                   8          8  4  0   6  0  0   1  0  0

    :param index: position of a number/cell in list of sudoku grid.
    :return: row, column, and sub square indexes.
    """
    row_index = index // 9
    col_index = index % 9
    sub_index = row_index // 3 * 3 + col_index // 3

    return row_index, col_index, sub_index


def find_possible_numbers_for_cell(index, puzzle_grid):
    """Find possible solution numbers for each cell. if given index has already value other than 0, the function returns
    the value immediately. If value of given index is 0 it means the cell needs to be solved. For all possible numbers
    between 1 and 9, if number is in associate row, column and sub square of given index, the nuber is not possible
    solution, and is removed from possibles. If there is no possible solution for a given index (cell), it means puzzle
    is not solvable.

    :param index: position of a cell in puzzle grid (int).
    :param puzzle_grid: list of 81 numbers  which represents sudoku puzzle.
    :return: list of possible solutions for a given cell(index) in a given sudoku puzzle.
    """
    possibles = [i for i in range(1, 10)]

    (puzzle_grid_row, puzzle_grid_col, puzzle_grid_sub) = get_grids(puzzle_grid)
    (row_index, col_index, sub_index) = find_coordinates(index)

    # if given cell has value, it means, it this cell has only one possible number.
    if puzzle_grid[index]:
        return [puzzle_grid[index]]
    else:
        for i in range(1, 10):

            if i in puzzle_grid_row[row_index]:
                possibles.remove(i)
            elif i in puzzle_grid_col[col_index]:
                possibles.remove(i)
            elif i in puzzle_grid_sub[sub_index]:
                possibles.remove(i)

    return possibles


def solve(puzzle, i=0):
    """Solves sudoku puzzle for given cell (i) in a puzzle grid. it checks four possibilities:
        1- given puzzle contains a cell with no possible solutions, it means puzzle is unsolvable (Return False)
        2- possible solutions for a given cell is only one number, function inserts that number immediately (next i)
        3- there are multiple solutions for a given cell, function pickes one of them and solve the puzzle for that
            guess if it's solvable, it goes to next cell, if not, it takes another guess among possible.
        4- index is 80, it means all the cells are evaluated (solved), it means puzzle is solved (return solution)

    :param puzzle: list of 81 numbers in a sudoku puzzle grid.
    :param i: index or position of a cell in puzzle.
    :return: result of solving sudoku puzzle.
    """
    # copies puzzle list into bew variable puzzle_grid (to avoid over writing into original puzzle)
    puzzle_grid = puzzle[:]

    while True:

        # finds possible numbers for given cell
        possibles = find_possible_numbers_for_cell(i, puzzle_grid)

        # if there is no possibles, returns false (puzzle is unsolvable)
        if not possibles:
            return False

        # if index is 80 (last cell), just need to insert single possible value for last cell and return the puzzle_grid
        # puzzle is solved here.
        if i == 80:
            puzzle_grid[80] = possibles[0]
            return puzzle_grid

        # if there is more than one possible solutions for given cell break and go for making guess among possibles.
        if len(possibles) > 1:
            break

        # if there is only one possible solution for a given cell, insert it into the puzzle grid.
        if len(possibles) == 1:
            puzzle_grid[i] = possibles[0]

        i += 1

    # makes guess among possibles for a given cell (i), and checks puzzle resolvability for next cell (i+1)
    for guess in possibles:
        puzzle_grid[i] = guess
        result = solve(puzzle_grid, i + 1)
        if result:
            return result
    return False


def print_sudoku(puzzle):
    """Prints givens sudoku puzzle list in format of 2D array matrix. For example it prints sudoku grid below in
     9X9 matrix:
     given puzzle list : [0, 0, 4, 0, 0, 6, 0, 7, 9, 0, 0, 0, 0, 0, 0, 6, 0, 2, 0, 5, 6, 0, 9, 2, 3, 0, 0, 0, 7, 8, 0,
     6, 1, 0, 3, 0, 5, 0, 9, 0, 0, 0, 4, 0, 6, 0, 2, 0, 5, 4, 0, 8, 9, 0, 0, 0, 7, 4, 1, 0, 9, 2, 0, 1, 0, 5, 0, 0,
     0, 0, 0, 0, 8, 4, 0, 6, 0, 0, 1, 0, 0]

     it prints :

     0  0  4   0  0  6   0  7  9
     0  0  0   0  0  0   6  0  2
     0  5  6   0  9  2   3  0  0

     0  7  8   0  6  1   0  3  0
     5  0  9   0  0  0   4  0  6
     0  2  0   5  4  0   8  9  0

     0  0  7   4  1  0   9  2  0
     1  0  5   0  0  0   0  0  0
     8  4  0   6  0  0   1  0  0

    :param puzzle: list of 81 numbers in a sudoku puzzle grid.
    :return: None
    """
    for i in range(9):
        for j in range(9):
            print(puzzle[i*9 + j], end="  ")
            if (j+1) % 3 == 0:
                print('', end=" ")
        if (i+1) % 3 == 0:
            print()
        print()


def sudoku(sudoku_string):
    """Solves a sudoku puzzle given in string of 81 numbers. it prints the puzzle and its solution. if it is unsolvable,
     it prints "Unsolvable".

    :param sudoku_string:
    :return: None
    """
    # converts string of numbers into list of numbers.
    puzzle_input = [int(num) for num in sudoku_string]

    print('Puzzle')

    print_sudoku(puzzle_input)

    if solve(puzzle_input, 0):
        print('Solved')
        print_sudoku(solve(puzzle_input))
    else:
        print("Unsolvable")


def main():
    # calls sudoku to solve given sudoku string. input you puzzle in string format (81 numbers) and run the application.
    sudoku('004006079000000602056092300078061030509000406020540890007410920105000000840600100')


if __name__ == "__main__":
    main()
