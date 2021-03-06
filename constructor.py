# 3rd Party Packages
# from typing import Union, Dict
import numpy as np

# We use backtracking on the position of the clue numbers, checking for validity each time
# number_grid's have 0's and clue numbers in the entries
# word_grid's have '' (unconfimed), '-' (confirmed blank) and letters in the entries

# Largest possible number that a clue could take
max_clue_num = 1000


def func_with_empty(function, iterable, fill=0):
    """Applies a function to an iterable, with a default value if empty"""
    if len(iterable) == 0:
        return fill
    else:
        return function(iterable)


@np.vectorize
def check_overlap(a: str, b: str) -> bool:
    """Can a and b overlap?"""
    return (a == "") or (b == "") or (a == b)


def update_grid(grid: np.ndarray, answer: str, start: (int, int), is_across: bool) -> None:
    """direction=True for across, False for down"""
    word_length = len(answer)

    if is_across:
        if start[1] + word_length > grid.shape[1]:
            raise ValueError("Word is too long to be added here")
        prepend_dash = (start[1] > 0)
        append_dash = (start[1] + word_length < grid.shape[1])
        grid_indices = start[0], slice(start[1] - prepend_dash, start[1] + len(answer) + append_dash)
    else:
        if start[0] + word_length > grid.shape[0]:
            raise ValueError("Word is too long to be added here")
        prepend_dash = (start[0] > 0)
        append_dash = (start[0] + word_length < grid.shape[0])
        grid_indices = slice(start[0] - prepend_dash, start[0] + len(answer) + append_dash), start[1]

    old_grid = grid[grid_indices]
    new_grid = np.array(['-'] * prepend_dash + list(answer) + ['-'] * append_dash)

    if not np.all(check_overlap(old_grid, new_grid)):
        raise ValueError("New word disagrees with a letter in the grid")
    else:
        grid[grid_indices] = new_grid

    # Sanity checking the times crossing style basically boils down to "is there a 2 x 2 box filled with letters"?
    if is_across:
        for index in range(start[1], start[1] + word_length - 1):
            if start[0] < grid.shape[0] - 1:
                square_test = len(''.join(grid[start[0]:start[0] + 2, index:index + 2].reshape(4)).replace('-', ''))
                if square_test == 4:
                    raise ValueError("Adjacent across clues")
            if start[0] > 0:
                square_test = len(''.join(grid[start[0] - 1:start[0] + 1, index:index + 2].reshape(4)).replace('-', ''))
                if square_test == 4:
                    raise ValueError("Adjacent across clues")
    else:
        for index in range(start[0], start[0] + word_length - 1):
            if start[1] < grid.shape[1] - 1:
                square_test = len(''.join(grid[index:index + 2, start[1]:start[1] + 2].reshape(4)).replace('-', ''))
                if square_test == 4:
                    raise ValueError("Adjacent down clues")
            if start[1] > 0:
                square_test = len(''.join(grid[index:index + 2, start[1] - 1:start[1] + 1].reshape(4)).replace('-', ''))
                if square_test == 4:
                    raise ValueError("Adjacent down clues")


def constructor(grid_size, across_clues, down_clues):
    number_grid = np.zeros((grid_size, grid_size), dtype=np.int16)
    word_grid = np.zeros((grid_size, grid_size), dtype=str)

    try:
        assert len(across_clues) > 0
        assert len(down_clues) > 0
    except AssertionError:
        raise ValueError("Crossword not completely filled - something might have gone wrong getting the clues")

    answer = backtracker(number_grid, word_grid, across_clues, down_clues)

    # Add some validation:
    for i in range(1, max(max(across_clues), max(down_clues)) + 1):
        if i not in answer[0]:
            raise ValueError("Crossword not completely filled - something might have gone wrong getting the clues")

    return answer


def backtracker(number_grid: np.ndarray, word_grid: np.ndarray, across_clues: dict, down_clues: dict) -> (np.ndarray, np.ndarray):
    if len(across_clues) + len(down_clues) == 0:
        return number_grid, word_grid

    # Copy everything so we don't modify ducts above
    ngrid = number_grid.copy()

    clue_num = min(func_with_empty(min, across_clues, max_clue_num), func_with_empty(min, down_clues, max_clue_num))
    start_row_index, start_col_index = np.unravel_index(ngrid.argmax() + (clue_num != 1), ngrid.shape)

    for row_index in range(start_row_index, ngrid.shape[0]):
        for col_index in range(start_col_index if row_index == start_row_index else 0, ngrid.shape[1]):
            ngrid[row_index, col_index] = clue_num
            wgrid = word_grid.copy()
            across = across_clues.copy()
            down = down_clues.copy()

            for clues, is_across in [(across, True), (down, False)]:
                if clue_num in clues:
                    answer = clues.pop(clue_num)[0]
                    try:
                        update_grid(wgrid, answer, (row_index, col_index), is_across)
                    # i.e. word doesn't fit grid/contradicts existing letters
                    except ValueError:
                        break
            else:
                # If clues were successfully added
                forward_search = backtracker(ngrid, wgrid, across, down)
                if forward_search is not None:
                    return forward_search

            ngrid[row_index, col_index] = 0
