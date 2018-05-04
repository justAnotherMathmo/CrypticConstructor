import sys
import collector
import constructor
import drawer

if __name__ == '__main__':
    grid_size = 13 # sys.argv[1]
    url = r'https://times-xwd-times.livejournal.com/1935273.html' # sys.argv[2]
    across_clues, down_clues = collector.get_parsed_clues(url)

    crossword_grid = constructor.constructor(grid_size, across_clues, down_clues)

    print(drawer.drawer(crossword_grid, across_clues, down_clues))
