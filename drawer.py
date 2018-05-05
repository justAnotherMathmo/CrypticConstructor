import numpy as np
import turtle

vector_len = np.vectorize(len)
ascii_empty =  '..'
ascii_shaded = '%%'


def solution_drawer(word_grid):
    wgrid = word_grid.copy()
    wgrid[wgrid == ''] = '-'
    return wgrid


def ascii_drawer(num_grid, word_grid, across_clues, down_clues):
    wgrid = word_grid.astype('<U2')

    # First fill all empty strings with dashes
    wgrid[(wgrid == '') | (wgrid == '-')] = ascii_shaded

    # Then replace all letters with ?
    wgrid[wgrid != ascii_shaded] = ascii_empty

    # Finally fill with the numbers and pad with 0's
    wgrid[num_grid != 0] = num_grid[num_grid != 0]
    wgrid[vector_len(wgrid) < 2] = ['0' + str(i) for i in range(1, 10)]

    return wgrid


def draw_box(t, x, y, size, fill_color):
    t.penup()
    t.goto(x, y)
    t.pendown()

    t.fillcolor(fill_color)
    t.begin_fill()  # Shape drawn after this will be filled with this color!

    for i in range(0, 4):
        t.forward(size) # move forward
        t.right(90) # turn pen right 90 degrees

    t.end_fill() # Go ahead and fill the rectangle!


def drawer(num_grid, word_grid, across_clues, down_clues):
    # print(num_grid)
    # return solution_drawer(word_grid)
    return ascii_drawer(num_grid, word_grid, across_clues, down_clues)
