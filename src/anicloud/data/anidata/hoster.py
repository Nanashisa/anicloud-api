from enum import Enum
from urllib.parse import urlencode

from anicloud.networking.load import Loader


class Language(Enum):
    GERMAN = 1
    ENGLISH_SUB = 2
    GERMAN_SUB = 3


class ReportReason(Enum):
    MISSING_404 = 1
    WRONG_EPISODE = 2
    SOUND_ERROR = 3
    WRONG_LANGUAGE = 4
    OTHER = 5


class Hoster:
    def __init__(self, url: str, name: str, lang: Language):
        self.url: str = url
        self.id: int = int(url.strip('/').split("/")[-1])
        self.name: str = name
        self.lang = lang
    
    def report(self, reason: ReportReason, otherInfo: str, lo: Loader):
        req = lo.post("https://anicloud.io/ajax/reportLink", urlencode({
            "link": self.id,
            "reason": int(reason.value),
            "extra": int(self.lang.value if reason == ReportReason.WRONG_LANGUAGE else 0),
            "moreInformation": otherInfo
        }))
        if req.status_code == 200:
            return req.json()["status"]
        return False
    
    def __str__(self):
        return self.name
    # TODO
