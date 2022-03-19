from bs4 import BeautifulSoup

from anicloud.data.anidata.anime import Anime
from ..networking.load import Loader


class Index(Loader):
    def __init__(self, lo: Loader):
        super().__init__(lo)
        html = BeautifulSoup(self.load("https://anicloud.io/animes").text, features="html.parser")
        genres = html.select("div.genre")
        self.list = []
        for genre in genres:
            group_name = genre.select_one("h3").text
            entries = genre.select("ul li a")
            for entry in entries:
                self.list.append(Anime(entry.attrs["href"], "index", title=entry.text.strip(), genres=[group_name]))
    
    def search(self, s: str) -> list[Anime]:
        return [x for x in self.list if x.title.__contains__(s)]
