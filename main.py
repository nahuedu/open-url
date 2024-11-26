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
        con.row_factory = dict_factory
        cur = con.cursor()

        return step.MostVisitedStep(finder).process(cur, search, size_top_visited) + step.RecentsStep(finder).process(cur, search, size_recents)

def debug(search):
    finder = get_finder('orion', None)

    data_path = 'data/hist'
    shutil.copyfile(finder.dir, data_path, follow_symlinks=False)

    with sqlite3.connect(data_path) as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        st = step.MostVisitedStep(finder)

        cur.execute(st.get_query(search, 3), st.params(search))
        return cur.fetchall()

def dict_factory(cursor, row):
    fields = [column[0].lower() for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


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
