import re
from bs4 import BeautifulSoup

from anicloud.data.anidata.anime import Anime
from ..networking.load import Loader
from ..util.dateparser import parse as parse_date
from ..util.language_parser import parse_lang


class Calendar(Loader):
    def __init__(self, lo: Loader):
        super().__init__(lo)
        html = BeautifulSoup(lo.load("https://anicloud.io/animekalender").text, features="html.parser")
        days = html.select("section.calendarList")
        self.list = []
        for day in days:
            date = re.search(r"(?<=\s)[0-9]{2}\.[0-9]{2}\.[0-9]{4}", day.select_one("h3").text).group()
            entries = \
                day.select("div.seriesListContainer.row a[target=\"_blank\"][title=\"\"][href^=\"/anime/stream/\"]")
            for entry in entries:
                episode_season = re.search("S(?P<s>[0-9]{2,})E(?P<e>[0-9]{2,})", entry.select("small")[0].text)
                time = re.search("[0-9]{2}:[0-9]{2}", entry.select("small")[1].text).group()
                self.list.append(
                        Anime(entry.attrs["href"], "calendar",
                              title=entry.select(".seriesTitle")[0].text.strip(),
                              cover=entry.select("img[data-src^=\"/public/img/cover/\"]")[0].attrs["data-src"],
                              season=int(episode_season.group("s")),
                              episode=int(episode_season.group("e")),
                              lang=parse_lang(entry.select_one(
                                      "small noscript img.flag").attrs["src"].split("/")[-1].split(".")[0]),
                              date_out=parse_date(date + " " + time))
                )
                del episode_season
                del time
