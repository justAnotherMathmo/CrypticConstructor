import numpy as np
import turtle

vector_len = np.vectorize(len)
ascii_empty =  '..'
ascii_shaded = '%%'


def solution_drawer(word_grid):
    wgrid = word_grid.copy()
    wgrid[wgrid == ''] = '-'
    print(wgrid)


def ascii_drawer(num_grid, word_grid, across_clues, down_clues):
    wgrid = word_grid.astype('<U2')

    # First fill all empty strings with dashes
    wgrid[(wgrid == '') | (wgrid == '-')] = ascii_shaded

    # Then replace all letters with ?
    wgrid[wgrid != ascii_shaded] = ascii_empty

    # Finally fill with the numbers and pad with 0's
    wgrid[num_grid != 0] = num_grid[num_grid != 0]
    wgrid[vector_len(wgrid) < 2] = ['0' + str(i) for i in range(1, 10)]

    print(wgrid)


def _draw_box(t: turtle.Turtle,
              x: float, y: float,
              size: float,
              fill_color: str,
              small_text: int=0, large_text: str='') -> None:
    t.penup()
    t.goto(x, y)
    t.pendown()

    t.fillcolor(fill_color)
    t.begin_fill()  # Shape drawn after this will be filled with this color!

    for i in range(4):
        t.forward(size)
        t.right(90)

    t.end_fill()
    if small_text != 0:
        t.penup()
        t.goto(x + size / 8, y - size / 2.2)
        t.write(small_text)
    if large_text != '':
        t.penup()
        t.goto(x + size / 1.9, y - size)
        t.write(large_text, align='center', font=("Arial", 15, "normal"))


def turtle_drawer(num_grid: np.ndarray, word_grid: np.ndarray=None,
                  across_clues: dict=None, down_clues: dict=None,
                  write_clues: bool=True) -> None:
    board_size = num_grid.shape
    c = ('white', 'black')
    board = turtle.Turtle()
    board.speed(0)
    start_x = -100
    start_y = 300
    box_size = 30
    for i in range(board_size[0]):
        for j in range(board_size[1]):
            _draw_box(board,
                      start_x + j*box_size, start_y - i*box_size, box_size,
                      c[1] if (word_grid[i, j] in ['', '-']) else c[0],
                      num_grid[i, j])

    if write_clues:
        y_pos = 300
        x_pos = -500
        clue_width = 60
        small_step = 15
        small_font = 10
        large_step = 20
        large_font = 14
        board.penup()
        board.goto(x_pos - 25, y_pos)
        board.write('ACROSS', font=('Arial', large_font, "bold"))
        y_pos -= large_step

        def clue_writer(clues):
            y = y_pos
            for idx in sorted(clues.keys()):
                clue = clues[idx][1]
                clue_split = clue_splitter(clue, clue_width)
                for clue_frac in clue_split:
                    board.goto(x_pos, y)
                    board.write(f'{idx}: {clue_frac}', font=('Arial', small_font, "normal"))
                    y -= small_step
            return y

        y_pos = clue_writer(across_clues)
        y_pos -= small_step

        board.goto(x_pos - 25, y_pos)
        board.write('DOWN', font=('Arial', large_font, "bold"))
        y_pos -= large_step
        y_pos = clue_writer(down_clues)

    board.hideturtle()
    turtle.done()


def clue_splitter(clue: str, clue_width: int=35) -> list:
    clue_split = clue.split(' ')
    rows = ['']
    for idx, clue_word in enumerate(clue_split):
        if (len(rows[-1]) + len(clue_word) > clue_width) and (idx != len(clue_split) - 1):
            rows.append('')
        rows[-1] += ' ' + clue_word
    return rows


def drawer(num_grid, word_grid, across_clues, down_clues):
    # print(num_grid)
    # return solution_drawer(word_grid)
    return turtle_drawer(num_grid, word_grid, across_clues, down_clues)
    # return ascii_drawer(num_grid, word_grid, across_clues, down_clues)
