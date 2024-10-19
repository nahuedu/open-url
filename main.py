import sqlite3
from pathlib import Path
import json
from sys import argv

dir = Path("~/Library/Application Support/Orion/Defaults/history").expanduser()
size = 10

def main():
   search = argv[1]
   terms = words(search)

   con = sqlite3.connect(str(dir))
   cur = con.cursor()

   cur.execute(query(terms), params(terms))
   records = cur.fetchall()

   print(json.dumps(output(records), ensure_ascii=False))

def words(search):
   return list(map(lambda w: f"%{w}%", search.split()))


def params(words):
    return tuple(words)

def query(words):
    base = "select * from history_items"
    where = "where"
    filters = " and ".join(list(map(lambda a: "title like ?", range(len(words)))))
    order = "order by visit_count desc"
    limit = f"limit {size}"

    return " ".join([base, where, filters, order, limit])

def output(records):
    return {
        "items": list(map(elem, records))
    }

def elem(record):
    title = record[2]
    url = record[1]

    return {
        "title": title,
        "subtitle": url,
        "arg": url
    }

if __name__ == "__main__":
    main()