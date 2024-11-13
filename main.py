import json
import plistlib
import sqlite3
from pathlib import Path
from sys import argv
import shutil

from finder import Chrome, Finder, Orion

bmDir = Path(
    "~/Library/Application Support/Orion/Defaults/favourites.plist"
).expanduser()


def main(browser, search, size, chrome_dir):
    records = execute_query(browser, search, size, chrome_dir)
    print(json.dumps(output(records), ensure_ascii=False))


def debug_query(browser, search, size, chrome_dir):
    print(json.dumps(execute_query(browser, search, size, chrome_dir), ensure_ascii=False))


def execute_query(browser, search, size, chrome_dir):
    finder = get_finder(browser, chrome_dir)

    data_path = 'data/hist'
    shutil.copyfile(finder.dir, data_path, follow_symlinks=False)

    con = sqlite3.connect(data_path)
    cur = con.cursor()

    cur.execute(finder.query(search, size), params(finder.words(search)))
    return cur.fetchall()


def get_finder(browser, chrome_dir):
    if browser == "chrome":
        return Chrome(chrome_dir)

    if browser == "orion":
        return Orion()

    return Finder()


def debug():
    with open(bmDir, "rb") as f:
        data = json.dumps(plistlib.load(f), default=lambda a: str(a))
        print(data)


def params(words):
    return tuple(words) + tuple(words)


def output(records):
    return {"items": list(map(elem, records))}


def elem(record):
    title = record[0]
    url = record[1]

    return {
        "title": title,
        "subtitle": url,
        "arg": url,
        "icon": {
            "path": "img/logo.png"
        }
    }


if __name__ == "__main__":
    chrome_dir = argv[4]
    size_most_visited = argv[3]
    browser = argv[2]
    search = argv[1]

    size_recents = 3

    main(browser, search, size_most_visited, chrome_dir)
