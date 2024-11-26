from pathlib import Path


class Finder:
    def __init__(self):
        self.dir = ""

    def query_top_visited(self, search, size):
        order = f"order by {self.order_column_top_visited()} desc"

        return self.query(search, size, order)

    def query_recents(self, search, size):
        order = f"order by {self.order_column_recents()} desc"

        return self.query(search, size, order)

    def query(self, search, size, order):
        select = f"select *"
        fm = f"from {self.table()}"
        where = f"where ({self.filters(self.words(search))})"
        limit = f"limit {size}"

        return " ".join([select, fm, where, order, limit])


    def filters(self, words):
        title_filter = self.filter_block(words, "and", self.title_column())
        host_filter = self.filter_block(words, "and", self.host_column())

        return f"({title_filter}) or ({host_filter})"

    def filter_block(self, words, op, column):
        return f" {op} ".join(
            list(map(lambda a: f"{column} like ?", range(len(words))))
        )

    def words(self, search):
        return list(map(lambda w: f"%{w}%", search.split()))

    def order_column_recents(self) -> str:
        return "last_visit_time"

    def order_column_top_visited(self) -> str:
        return "visit_count"

    def title_column(self) -> str:
        return "title"

    def host_column(self) -> str:
        return ""

    def table(self) -> str:
        return ""

    def url_column(self) -> str:
        return "url"


class Orion(Finder):
    def __init__(self):
        self.dir = Path("~/Library/Application Support/Orion/Defaults/history").expanduser()

    def host_column(self):
        return "host"

    def table(self):
        return "history_items"


class Chrome(Finder):
    def __init__(self, profile_dir):
        self.dir = Path(f"~/Library/Application Support/Google/Chrome/{profile_dir}/History").expanduser()


    def host_column(self):
        return "url"

    def table(self):
        return "urls"
