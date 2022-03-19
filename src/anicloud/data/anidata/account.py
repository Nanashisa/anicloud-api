import re

from bs4 import BeautifulSoup


# from anicloud.networking.load import Loader TODO
from anicloud.util.emoji_parser import parse_emojis


class Account:
    def __init__(self, uri_or_username: str, username: str = None):
        self.is_online = None
        self.back_img = None
        self.img = None
        self.user_id = None
        self.rank = None
        self.desc = None
        self.watched = None
        self.friends = None
        self.username = username
        self.subscr = None
        self.list_count = None
        self.reg_date = None
        self.website = None
        self.place = None
        self.uri = uri_or_username
        if not self.uri.__contains__("/"):
            self.uri = "https://anicloud.io/user/profil/" + self.uri.lower()
    
    def load(self, lo):  # TODO
        req = lo.load(self.uri)
        if req.url.endswith("/profil/notFound"):
            return False
        html = BeautifulSoup(req.text, features="html.parser")
        self.username = html.select_one("div.userDetailBackground a[href^=\"/user/profil/\"] h1").text.strip()
        self.rank = html.select_one("div.userDetailBackground div.userDetailRank").text.strip()
        self.desc = parse_emojis(html.select_one("div.userDetailBackground p.userDetailDescription").text)
        self.watched = html.select_one(
                "div.userDetailStatistics a[href^=\"/user/profil/\"][href$=\"/watched\"] span").text
        self.friends = html.select_one(
                "div.userDetailStatistics a[href^=\"/user/profil/\"][href$=\"/freunde\"] span").text
        place = html.select_one("ul.userDetailList li i.fa-map-marker")
        self.place = None if place is None else parse_emojis(place.parent.text.strip())
        website = html.select_one("ul.userDetailList li i.fa-link")
        self.website = None if website is None else website.parent.select_one("a").attrs["href"].strip()
        reg_date = html.select_one("ul.userDetailList li i.fa-calendar-check")
        self.reg_date = None if reg_date is None else [re.search(
            r"(?P<month>Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember) "
            r"(?P<year>[0-9]{4})",
            reg_date.parent.text).groupdict()[key] for key in ["month", "year"]]
        list_count = html.select_one("ul.userDetailList li i.fa-list-ul")
        self.list_count = None if list_count is None else re.search(r"[0-9]+", list_count.parent.text.strip()).group()
        subscr = html.select_one("ul.userDetailList li i.fa-volume-up")
        self.subscr = None if subscr is None else re.search(r"[0-9]+", subscr.parent.text.strip()).group()
        self.user_id = html.select_one("section#userDetails").attrs["data-user-id"]
        self.img = html.select_one("img.userDetailProfilePicture").attrs["data-src"]
        self.back_img = re.search(r"(?<=')/public/img/profil/background/[^']+(?=')", str(html)).group()
        self.is_online = len(html.select(
                "div.userDetailBackground a[href^=\"/user/profil/\"] h1 span.userStatusOnline.pulse")) > 0
        return True
    
    def friend_request(self, lo):  # TODO
        if not lo.authed:
            return False
        return lo.post("https://anicloud.io/ajax/friendshipRequest", f"userID={self.user_id}").status_code == 200
    
    def __str__(self):
        return f"{self.username}"
