import re
from urllib.parse import urlencode, urljoin

from bs4 import BeautifulSoup

from .hoster import Hoster, Language
from anicloud.networking.load import Loader
from ...util.language_parser import parse_lang


class Episode:
    def __init__(self, uri: str, desc: str = None, season: int = None, episode: int = None, title: str = None,
                 hosters: list[str] = None, langs: list[Language] = None, episode_id: int = None, seen: bool = None):
        self.id: int = episode_id
        self.seen: bool = seen
        self.season: int = season
        self.episode: int = episode
        self.title: str = title
        self.desc: str = desc
        self.uri: str = uri
        self.hosters: list[str] = hosters
        self.langs: list[Language] = langs
        self.loaded = False
    
    def load(self, lo: Loader):
        html_raw = lo.load(urljoin("https://anicloud.io", self.uri)).text
        html = BeautifulSoup(html_raw, features="html.parser")
        self.desc = html.select_one("p[itemprop=\"accessibilitySummary\"]").attrs["data-full-description"]
        self.season = \
            html.select_one("div[itemprop=\"containsSeason\"] meta[itemprop=\"seasonNumber\"]").attrs["content"]
        self.episode = html.select_one("div[itemprop=\"containsSeason\"] meta[itemprop=\"episode\"]").attrs["content"]
        self.title = (html.select_one("div.hosterSiteTitle h2 span")
                      if html.select_one("div.hosterSiteTitle h2 span") is not None else
                      html.select_one("div.hosterSiteTitle h2 small")).text
        self.id = int(html.select_one("div.hosterSiteTitle[data-episode-id]").attrs["data-episode-id"])
        self.seen = bool(re.search(r"<li>\s*<a(?:[^>]+class=\"(?:active|seen)\"){2}(?:[^>]+>){3}", html_raw))
        self.desc = html.select_one("div.hosterSiteTitle p[itemprop=\"description\"]").text
        self.langs = [
            parse_lang(img.attrs["src"].split("/")[-1].split(".")[0])
            for img in html.select("div.changeLanguageBox img[src^=\"/public/img/\"][src$=\".svg\"]")
        ]
        self.hosters = [
            Hoster(hoster.attrs["href"],
                   hoster.select_one("h4").text, Language(int(hoster.parent.parent.attrs["data-lang-key"])))
            for hoster in html.select("div.generateInlinePlayer a[itemprop=\"url\"]")
        ]
        self.loaded = True
    
    def toggle_seen(self, lo: Loader) -> bool:
        return lo.post("https://anicloud.io/ajax/watchEpisode", urlencode({"episode": self.id})).json()["status"]
    
    def __str__(self):
        return f"Episode: \"{(self.title if self.title is not None else self.uri)}\""
