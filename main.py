import sys
import collector
import constructor
import drawer

if __name__ == '__main__':
    grid_size = sys.argv[1]  # 13
    url = sys.argv[2]  # r'https://times-xwd-times.livejournal.com/1935273.html'
    across_clues, down_clues = collector.get_parsed_clues(url)

    num_grid, word_grid = constructor.constructor(grid_size, across_clues, down_clues)

    print(drawer.drawer(num_grid, word_grid, across_clues, down_clues))
