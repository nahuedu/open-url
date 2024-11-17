import json
import plistlib
import sqlite3
from pathlib import Path
from sys import argv
import shutil
import step

from finder import Chrome, Finder, Orion

bmDir = Path(
    "~/Library/Application Support/Orion/Defaults/favourites.plist"
).expanduser()


def main(browser, search, size_top_visited, chrome_dir, size_recents):
    results = execute_query(browser, search, size_top_visited, chrome_dir, size_recents)
    print(json.dumps(output(results), ensure_ascii=False))


def execute_query(browser, search, size_top_visited, chrome_dir, size_recents):
    finder = get_finder(browser, chrome_dir)

    data_path = 'data/hist'
    shutil.copyfile(finder.dir, data_path, follow_symlinks=False)

    with sqlite3.connect(data_path) as con:
        cur = con.cursor()

        return step.MostVisitedStep().process(cur, finder, search, size_top_visited) + step.RecentsStep().process(cur, finder, search, size_recents)



def get_finder(browser, chrome_dir):
    if browser == "chrome":
        return Chrome(chrome_dir)

    if browser == "orion":
        return Orion()

    return Finder()


def output(elements):
    return {"items": list(elements)}


if __name__ == "__main__":
    chrome_dir = argv[4]
    size_top_visited = argv[3]
    browser = argv[2]
    search = argv[1]

    size_recents = 3

    main(browser, search, size_top_visited, chrome_dir, size_recents)
