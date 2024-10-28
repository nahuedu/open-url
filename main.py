import json
import plistlib
import sqlite3
from pathlib import Path
from sys import argv

from finder import Chrome, Finder, Orion

bmDir = Path(
    "~/Library/Application Support/Orion/Defaults/favourites.plist"
).expanduser()


def main(browser, search, size):
    records = execute_query(browser, search, size)
    print(json.dumps(output(records), ensure_ascii=False))


def debug_query(browser, search, size):
    print(json.dumps(execute_query(browser, search, size), ensure_ascii=False))


def execute_query(browser, search, size):
    finder = get_finder(browser)

    con = sqlite3.connect(finder.dir)
    cur = con.cursor()

    cur.execute(finder.query(search, size), params(finder.words(search)))
    return cur.fetchall()


def get_finder(browser):
    if browser == "chrome":
        return Chrome()

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

    return {"title": title, "subtitle": url, "arg": url}


if __name__ == "__main__":
    size_most_visited = argv[3]
    browser = argv[2]
    search = argv[1]
    size_recents = 3

    main(browser, search, size_most_visited)
