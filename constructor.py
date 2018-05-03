# 3rd Party Packages
import numpy as np
# Local
from . import collector


def constructor(grid_size, across_clues, down_clues):
    grid = np.zeros((grid_size, grid_size), dtype=str)

    # if 1 in down_clues and 1 in across_clues:
    #     update_grid(grid, across_clues[1][0], (0, 0), True)
    #     update_grid(grid, down_clues[1][0], (0, 0), False)
    # else:
    #     update_grid(grid, '-', (0, 0), False)

    return grid


def update_grid(grid, answer, start, direction):
    """direction=True for across, False for down"""
    if direction:
        grid[start[0], start[1]:start[1] + len(answer)] = list(answer)
    else:
        grid[start[0]:start[0] + len(answer), start[1]] = list(answer)
    return grid


def confirm_blank(grid, position):
    return update_grid(grid, '-', position, True)

