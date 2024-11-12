from pathlib import Path


class Finder:
    def __init__(self):
        self.dir = ""

    def query(self, search, size):
        select = f"select {self.title_column()}, {self.url_column()}"
        fm = f"from {self.table()}"
        where = f"where ({self.filters(self.words(search))})"
        order = f"order by {self.order_column()} desc"
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

    def order_column(self) -> str:
        return ""

    def title_column(self) -> str:
        return ""

    def host_column(self) -> str:
        return ""

    def table(self) -> str:
        return ""

    def url_column(self) -> str:
        return ""

    def get_url(self, record):
        return record[1]

    def get_title(self, record):
        return record[0]


class Orion(Finder):
    def __init__(self):
        self.dir = Path("~/Library/Application Support/Orion/Defaults/history").expanduser()


    def title_column(self):
        return "title"

    def host_column(self):
        return "host"

    def order_column(self):
        return "visit_count"

    def table(self):
        return "history_items"

    def url_column(self):
        return "url"


class Chrome(Finder):
    def __init__(self, profile_dir):
        self.dir = Path(f"~/Library/Application Support/Google/Chrome/{profile_dir}/History").expanduser()


    def title_column(self):
        return "title"

    def host_column(self):
        return "url"

    def order_column(self):
        return "visit_count"

    def table(self):
        return "urls"

    def url_column(self):
        return "url"
