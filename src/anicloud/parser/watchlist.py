from bs4 import BeautifulSoup

from anicloud.data.anidata.anime import Anime
from anicloud.exception.authentication import AuthenticationException
from anicloud.networking.load import Loader


class Watchlist(Loader):
    def __init__(self, lo: Loader):
        super().__init__(lo)
        if not self.authed:
            raise AuthenticationException
        html = BeautifulSoup(self.load("https://anicloud.io/account/watchlist").text, features="html.parser")
        entries = html.select("div.seriesListContainer div a[href^=\"/anime/stream/\"]")
        self.list = []
        for entry in entries:
            self.list.append(
                    Anime(entry.attrs["href"], "favourites",
                          title=entry.select_one("h3").text.strip(),
                          cover=entry.select_one("img[src^=\"/public/img/cover/\"]").attrs["src"],
                          genres=[entry.select_one("small").text])
            )
