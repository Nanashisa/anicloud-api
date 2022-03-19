import re
from bs4 import BeautifulSoup
from anicloud.networking.load import Loader


class AwesomeFontIconParser:
    def __init__(self, lo: Loader):
        self._dict = {}
        html = BeautifulSoup(lo.load("").text, features="html.parser")
        css = lo.load(html.select_one("head link[href$=\"fontawesome.min.css\"").attrs["href"]).text
        for icon in re.finditer(
                r"\.fa-(?P<name>[^:]+):before\s*{[^a-zA-Z0-9]*content:\"(?P<content>[^\"]+)\"[^}]*}", css):
            self._dict[icon.group("name")] = icon.group("content")
    
    def __getitem__(self, item):
        return self._dict[item]
    
