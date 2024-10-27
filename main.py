import json
import plistlib
import sqlite3
from pathlib import Path
from sys import argv

from finder import Chrome, Finder, Orion

bmDir = Path(
    "~/Library/Application Support/Orion/Defaults/favourites.plist"
).expanduser()

size = 10
browser = "orion"


def main():
    search = argv[1]
    browser = argv[2]

    finder = get_finder(browser)

    con = sqlite3.connect(finder.dir)
    cur = con.cursor()

    cur.execute(finder.query(search, size), params(finder.words(search)))
    records = cur.fetchall()

    print(json.dumps(output(records), ensure_ascii=False))


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
    title = record[2]
    url = record[1]

    return {"title": title, "subtitle": url, "arg": url}


if __name__ == "__main__":
    main()
