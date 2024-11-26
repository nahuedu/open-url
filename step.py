
class Step:
    def __init__(self, finder):
        self.finder = finder

    def elem(self, record):
        title = record[self.finder.title_column()]
        url = record[self.finder.url_column()]

        return {
            "title": title,
            "subtitle": self.subtitle(url),
            "arg": url,
            "icon": {
                "path": "img/logo.png"
            }
        }

    def subtitle(self, url):
        return ""

    def params(self, search):
        words = self.finder.words(search)
        return tuple(words) + tuple(words)

    def get_query(self, search, size):
        return ""

    def process(self, cursor, search, size):
        cursor.execute(self.get_query(search, size), self.params(search))
        records = cursor.fetchall()
        return list(map(self.elem, records))


class RecentsStep(Step):
    def __init__(self, finder):
        self.finder = finder

    def get_query(self, search, size):
        return self.finder.query_recents(search, size);

    def subtitle(self, url):
        return "Recents — " + url


class MostVisitedStep(Step):
    def __init__(self, finder):
        self.finder = finder

    def get_query(self, search, size):
        return self.finder.query_top_visited(search, size);

    def subtitle(self, url):
        return "Top visited — " + url
