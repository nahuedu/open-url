
class Step:

    def elem(self, record):
        title = record[0]
        url = record[1]

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

    def params(self, words):
        return tuple(words) + tuple(words)

    def get_query(self, finder, search, size):
        return ""

    def process(self, cursor, finder, search, size):
        cursor.execute(self.get_query(finder, search, size), self.params(finder.words(search)))
        records = cursor.fetchall()
        return list(map(self.elem, records))


class RecentsStep(Step):

    def get_query(self, finder, search, size):
        return finder.query_recents(search, size);

    def subtitle(self, url):
        return "Recents — " + url


class MostVisitedStep(Step):

    def get_query(self, finder, search, size):
        return finder.query_top_visited(search, size);

    def subtitle(self, url):
        return "Top visited — " + url
