import sys
import collector
import drawer

if __name__ == '__main__':
    try:
        grid_size = int(sys.argv[1])
        url = sys.argv[2]
    except IndexError:
        grid_size = 13
        url = r'https://times-xwd-times.livejournal.com/1935273.html'
    across_clues, down_clues = collector.get_parsed_clues(url)

    if len(sys.argv) > 3 and sys.argv[3] == 'sean':
        print('Using sean\'s method')
        import assembler
        answers = {(answer, 'A'): across_clues[answer][0] for answer in across_clues}
        for answer in down_clues:
            answers[(answer, 'D')] = down_clues[answer][0]
        num_grid, word_grid = assembler.assemble(answers, grid_size, True, True)
    else:
        import constructor
        num_grid, word_grid = constructor.constructor(grid_size, across_clues, down_clues)

    drawer.drawer(num_grid, word_grid, across_clues, down_clues)
