import html
import re
import requests


def _scrape_clues_type_1(url: str) -> list:
    req = requests.get(url)
    number_and_clue_regex = '<tr>\n<td valign="top">([0-9]+)</td>\n<td>(.*?)</td>\n</tr>'
    answer_regex = '<tr>\n<td.*?></td>\n<td><.*?>([A-Z- ]*)</.*?>(.*)</td>\n</tr>'
    regex_string = number_and_clue_regex + '\n' + answer_regex
    all_clues = re.findall(regex_string, req.text)

    return all_clues


def _scrape_clues_type_2(url: str) -> list:
    req = requests.get(url)
    number_and_clue_regex = '(?:<br />)+([0-9]+)\s*(.*?)<br />'
    answer_regex = ' *([A-Z- ]*) - (.*?)(?=<br />|</div>)+'
    regex_string = number_and_clue_regex + answer_regex
    all_clues = re.findall(regex_string, req.text)
    
    return all_clues


def parse_clue_tuple(clue_tuple: tuple) -> tuple:
    clue_number = int(clue_tuple[0])
    sanitised_clue = html.unescape(re.sub('<.*?>', '', clue_tuple[1]))
    answer = re.sub('[^A-Z]', '', clue_tuple[2])
    construction = html.unescape(clue_tuple[3])

    return clue_number, sanitised_clue, answer, construction


def get_parsed_clues(url: str) -> (dict, dict):
    dirty_clues = _scrape_clues_type_1(url)
    if len(dirty_clues) == 0:
        dirty_clues = _scrape_clues_type_2(url)
    across_clues = {}
    down_clues = {}

    last_clue_num = 0
    clue_dict = across_clues
    for dirty_clue in dirty_clues:
        try:
            clue = parse_clue_tuple(dirty_clue)
        except ValueError:
            # Clue parsing failed - probably picked up extra shit
            continue

        clue_num = clue[0]
        if clue_num < last_clue_num:
            clue_dict = down_clues
        last_clue_num = clue_num

        clue_dict[clue_num] = (clue[2], clue[1])

    return across_clues, down_clues


# Testing:
if __name__ == '__main__':
    print(get_parsed_clues(r'https://times-xwd-times.livejournal.com/1935273.html'))
