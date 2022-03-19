import datetime
from urllib.parse import urlencode, urljoin

from bs4 import BeautifulSoup

from .rating import Rating
from .actor import Actor
from .episode import Episode
from .country import Country
from .producer import Producer
from .director import Director
from .genre import Genre
from .season import Season
from anicloud.networking.load import Loader
from anicloud.util.episode_list_parser import parse_episode_list
from anicloud.data.anidata.hoster import Language


class Anime:
    def __init__(self, uri: str, origin: str, title: str = None, cover: str = None, genres: list[str] = None,
                 season: int = None, episode: int = None, lang: Language = None, date_out: datetime.datetime = None,
                 specials: list[Episode] = None, rating: Rating = None, directors: list[Director] = None,
                 imdb: str = None, countries: list[Country] = None, actors: list[Actor] = None,
                 producers: list[Producer] = None, age_restr: int = None, year_start: int = None, year_end: int = None,
                 desc: str = None, seasons: list[Season] = None, anime_id: int = None, favourite: bool = None,
                 watchlist: bool = None):
        self.favourite = favourite
        self.watchlist = watchlist
        self.specials: list[Episode] = specials
        self.id: int = anime_id
        self.rating: Rating = rating
        self.directors: list[Director] = directors
        self.imdb: str = imdb
        self.countries: list[Country] = countries
        self.actors: list[Actor] = actors
        self.producers: list[Producer] = producers
        self.age_restr: int = age_restr
        self.year_end: int = year_end
        self.year_start: int = year_start
        self.desc: str = desc
        self.cover: str = cover
        self.uri: str = uri
        self.genres: list[str] = genres
        self.title: str = title
        self.season: int = season
        self.episode: int = episode
        self.lang: Language = lang
        self.datetime: datetime = date_out
        self.origin: str = origin
        self.loaded = False
        self.seasons: list[Season] = seasons
    
    def load(self, lo: Loader):
        html = BeautifulSoup(lo.load(urljoin("https://anicloud.io", self.uri)).text, features="html.parser")
        self.id = int(html.select_one(".container .series-add .add-series").attrs["data-series-id"])
        self.watchlist = html.select_one(".container .series-add .add-series").attrs["data-series-watchlist"] == "1"
        self.favourite = html.select_one(".container .series-add .add-series").attrs["data-series-favourite"] == "1"
        self.desc = html.select_one("p[itemprop=\"accessibilitySummary\"]").attrs["data-full-description"]
        self.cover = html.select(".seriesCoverBox img[data-src^=\"/public/img/cover/\"]")[0].attrs["data-src"]
        self.title = html.select_one("div.series-title h1 span").text
        self.year_start = int(html.select_one("span[itemprop=\"startDate\"] a").text)
        self.year_end = int(0 if html.select_one("span[itemprop=\"endDate\"] a").text.lower() == "heute" else
                            html.select_one("span[itemprop=\"endDate\"] a").text)
        self.age_restr = int(html.select_one("div.fsk").attrs["data-fsk"])
        self.producers = [
            Producer(item.attrs["href"], item.select_one("span[itemprop=\"name\"]").text)
            for item in html.select("ul li[itemprop=\"creator\"] a[itemprop=\"url\"]")
        ]
        self.actors = [
            Actor(item.attrs["href"], item.select_one("span[itemprop=\"name\"]").text)
            for item in html.select("ul li[itemprop=\"actor\"] a[itemprop=\"url\"]")
        ]
        self.countries = [
            Country(item.attrs["href"], item.select_one("span[itemprop=\"name\"]").text)
            for item in html.select("ul li[itemprop=\"countryOfOrigin\"] a[itemprop=\"url\"]")
        ]
        self.directors = [
            Director(item.attrs["href"], item.select_one("span[itemprop=\"name\"]").text)
            for item in html.select("ul li[itemprop=\"director\"] a[itemprop=\"url\"]")
        ]
        self.genres = [
            Genre(item.attrs["href"], item.text)
            for item in html.select("div.genres ul[data-main-genre] li a[itemprop=\"genre\"]")
        ]
        self.imdb = html.select_one("a.imdb-link[href][data-imdb]").attrs["data-imdb"] if len(
                html.select("a.imdb-link[href][data-imdb]")) > 0 else None
        self.rating = Rating(int(html.select_one("span[itemprop=\"worstRating\"]").text),
                             int(html.select_one("span[itemprop=\"bestRating\"]").text),
                             int(html.select_one("span[itemprop=\"ratingValue\"]").text),
                             int(html.select_one("span[itemprop=\"ratingCount\"]").text))
        self.specials = None if "Refresh" in lo.session.head(
                urljoin("https://anicloud.io", self.uri + "/filme")).headers \
            else parse_episode_list(lo.load(urljoin("https://anicloud.io", self.uri)).text)
        i = 1
        if self.seasons is None:
            self.seasons = []
        while "Refresh" not in lo.session.head(urljoin("https://anicloud.io", self.uri + f"/staffel-{i}")).headers:
            self.seasons.append(Season(i, parse_episode_list(lo.load(
                    urljoin("https://anicloud.io", self.uri + f"/staffel-{i}")
            ).text), self.id))
            i += 1
        self.origin = "loaded"
        self.loaded = True
    
    def set_rating(self, lo: Loader, rating: Rating):
        return lo.post("https://anicloud.io/ajax/setRating",
                       urlencode({"series": self.id, "rating": rating.value - 1})).json()["status"]
    
    def toggle_favourite(self, lo: Loader):
        self.favourite = not self.favourite
        return lo.post("https://anicloud.io/ajax/setFavourite",
                       urlencode({"series": self.id})).json()["status"]
    
    def toggle_watchlist(self, lo: Loader):
        self.watchlist = not self.watchlist
        return lo.post("https://anicloud.io/ajax/setWatchList",
                       urlencode({"series": self.id})).json()["status"]
    
    def __str__(self):
        return "Anime: \"" + (self.title if self.title is not None else self.uri) + "\""
