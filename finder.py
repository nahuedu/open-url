from pathlib import Path


class Finder:
    def __init__(self):
        self.dir = ""

    def query(self, search, size):
        select = "select *"
        fm = f"from {self.fm()}"
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

    def fm(self) -> str:
        return ""


class Orion(Finder):
    def __init__(self):
        self.dir = str(
            Path("~/Library/Application Support/Orion/Defaults/history").expanduser()
        )

    def title_column(self):
        return "title"

    def host_column(self):
        return "host"

    def order_column(self):
        return "visit_count"

    def fm(self):
        return "history_items"


class Chrome(Finder):
    def __init__(self):
        self.dir = str(
            Path(
                "~/Library/Application Support/Google Chrome/Defaults/History"
            ).expanduser()
        )

    def title_column(self):
        return "title"

    def host_column(self):
        return "url"

    def order_column(self):
        return "visit_count"

    def fm(self):
        return "visits v join urls u on v.url = u.id"
