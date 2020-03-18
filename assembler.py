import numpy as np
import re


# flag that indicates when we should backtrack
class BacktrackException(Exception):
    pass


def backtrack_search(answers, size, symmetric):
    BLANK = ' '
    VOID = '#'

    # all letters in the completed grid
    board = np.array([[BLANK for j in range(size + 2)] for i in range(size + 2)])
    # all numbers labelling where answers start
    labels = np.array([[None for j in range(size + 2)] for i in range(size + 2)])
    for i in range(size + 2):
        board[0, i] = VOID
        board[size + 1, i] = VOID
        board[i, 0] = VOID
        board[i, size + 1] = VOID

    # separate across and down answers and sandwich with VOIDs
    across = {}
    down = {}
    for i, o in answers:
        ans = re.sub('[^A-Z]', '', answers[(i, o)])
        ans = VOID + ans + VOID
        if o == 'A':
            across[i] = ans
        else:
            down[i] = ans

    max_number = max(answers)[0]

    placements = []  # stack of placements, so we can backtrack as necessary

    # Undo the last placement
    def backtrack():
        if len(placements) > 0:
            label_placement, board_placement = placements.pop()
            for row, col in label_placement:
                labels[row, col] = None
            for row, col in board_placement:
                board[row, col] = BLANK

    # Try to write in the answer(s) numbered n (down or across or both) at position pos
    # Raises a BacktrackException if this fails because we try to overwrite non-BLANK squares
    def place(n, row, col):
        label_placement = []
        board_placement = []
        placements.append((label_placement, board_placement))
        try:
            assert labels[row, col] is None
            labels[row, col] = n
            label_placement.append((row, col))

            if n in across:
                ans = across[n]
                assert col + len(ans) <= size + 3  # word must fit
                for i, letter in enumerate(ans):
                    assert board[row, col - 1 + i] in [BLANK, letter]  # can't overwrite
                    if board[row, col - 1 + i] == BLANK:
                        board[row, col - 1 + i] = letter
                        board_placement.append((row, col - 1 + i))

                        down_special_logic(row, col - 1 + i)

            if n in down:
                ans = down[n]
                assert row + len(ans) <= size + 3  # word must fit
                for j, letter in enumerate(ans):
                    assert board[row - 1 + j, col] in [BLANK, letter]  # can't overwrite
                    if board[row - 1 + j, col] == BLANK:
                        board[row - 1 + j, col] = letter
                        board_placement.append((row - 1 + j, col))

        except AssertionError:
            raise BacktrackException

    # check the current board for symmetry
    def check_symmetry():
        for row in range(1, size + 1):
            for col in range(1, size + 1):
                first = board[row, col] in [BLANK, VOID]
                second = board[size + 1 - row, size + 1 - col] in [BLANK, VOID]
                if first != second:
                    raise BacktrackException

    # Down special logic: While writing in a new letter from an across, if we
    # write in a new letter immediately below another letter, this would imply
    # a down that we don't already have: this can't happen
    def down_special_logic(row, col):
        if board[row - 1, col] not in [BLANK, VOID]:
            raise BacktrackException

    # Across special logic: If board[row,col-1:col+2] looks like _XX, then we
    # must have an across answer starting at (row, col)
    def across_special_logic(row, col):
        if board[row, col - 1] in [BLANK, VOID]:
            if board[row, col] not in [BLANK, VOID]:
                if board[row, col + 1] not in [BLANK, VOID]:
                    if labels[row, col] not in across:
                        raise BacktrackException

    def publish():
        board_copy = board[1:-1, 1:-1]
        labels_copy = labels[1:-1, 1:-1]
        board_copy[board_copy == VOID] = BLANK
        return board_copy, labels_copy

    # recursive backtracker
    def backtracker(current_number, current_pos):
        for pos in range(current_pos, size ** 2):
            row, col = pos // size + 1, pos % size + 1

            if col >= 3:
                across_special_logic(row, col - 2)

            try:
                place(current_number, row, col)

                if current_number == max_number:
                    if symmetric:
                        check_symmetry()
                    yield publish()
                else:
                    yield from backtracker(current_number + 1, pos + 1)

            except BacktrackException:
                backtrack()

        # got to end of loop, so we must have gone wrong somewhere
        raise BacktrackException

    # start search
    yield from backtracker(1, 0)


def assemble(answers, size, symmetric=True, hide_answers=False):
    try:
        for board, labels in backtrack_search(answers, size, symmetric):
            if hide_answers:
                board[board != ' '] = '?'
            return board, labels
    except BacktrackException:
        raise BacktrackException('No solutions found. Check your answers or try increasing size')


def pretty_string(board, labels=None, hide_answers=False):
    size = board.shape[0]
    pretty_board = np.array([[None] * size] * size)
    for i in range(size):
        for j in range(size):
            if labels is not None and labels[i, j] is not None:
                pretty_board[i, j] = '{}:{}'.format(labels[i, j], board[i, j])
            else:
                pretty_board[i, j] = board[i, j]
            if hide_answers:
                pretty_board[i, j] = re.sub('[A-Z]', '?', pretty_board[i, j])

    lines = ['']
    for row in pretty_board:
        row = ('{:>4} ' * len(row)).format(*row)
        if hide_answers:
            row = re.sub('[A-Z]', '?', row)
        lines.append(row)
    lines.append('')
    return '\n'.join(lines)


def flatten(board, hide_answers=False):
    flat = ''.join([''.join(row) for row in board])
    if hide_answers:
        flat = re.sub('[A-Z]', '?', flat)
    return flat
