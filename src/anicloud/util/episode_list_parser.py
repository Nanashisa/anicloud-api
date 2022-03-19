from bs4 import BeautifulSoup

from .language_parser import parse_lang
from ..data.anidata.episode import Episode


def parse_episode_list(text: str) -> list[Episode]:
    html = BeautifulSoup(text, features="html.parser")
    season = int(html.select_one("meta[itemprop=\"seasonNumber\"]").attrs["content"])
    return [
        Episode(item.select_one("a[itemprop=\"url\"]").attrs["href"],
                title=item.select_one("td.seasonEpisodeTitle a strong").text,
                hosters=[
                    hoster.attrs["title"]
                    for hoster in item.select("td:not([class]) a i")
                ],
                langs=[
                    parse_lang(img.attrs["src"].split("/")[-1].split(".")[0])
                    for img in item.select("td.editFunctions a img.flag")
                ],
                episode=int(item.select_one("meta[itemprop=\"episodeNumber\"]").attrs["content"]),
                season=season)
        for item in html.select("table.seasonEpisodesList tbody tr[itemprop=\"episode\"]")
    ]
