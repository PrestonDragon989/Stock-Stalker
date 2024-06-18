import webbrowser as web


class OpenSite:
    def __init__(self):
        self.base_path = "https://prestondragon989.github.io/Stock-Stalker-Help/"
        self.file_ext = ".html"

        self.yahoo_site = "https://finance.yahoo.com/most-active/"

    def open_page(self, site):
        web.open(self.base_path + site + self.file_ext)

    def open_docs(self):
        web.open(self.base_path + "documentation" + self.file_ext)

    def open_yahoo(self):
        web.open(self.yahoo_site)
