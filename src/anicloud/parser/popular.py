from bs4 import BeautifulSoup

from anicloud.data.anidata.anime import Anime
from ..networking.load import Loader


class Popular(Loader):
    def __init__(self, lo: Loader):
        super().__init__(lo)
        html = BeautifulSoup(self.load("https://anicloud.io/beliebte-animes").text, features="html.parser")
        entries = html.select("div.seriesListContainer.row div[class^=\"col-\"] a[href^=\"/anime/stream/\"]")
        self.list = []
        for entry in entries:
            self.list.append(
                    Anime(entry.attrs["href"], "popular",
                          title=entry.select_one("h3").text.strip(),
                          cover=
                          entry.select_one("img[src^=\"data:\"][data-src^=\"/public/img/cover/\"]").attrs["data-src"],
                          genres=[entry.select_one("small").text])
            )
