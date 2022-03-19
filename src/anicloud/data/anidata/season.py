from urllib.parse import urlencode

from .episode import Episode
from ...networking.load import Loader


class Season:
    def __init__(self, season_number: int, episodes: list[Episode], anime_id: int):
        self.season_number = season_number
        self.episodes = episodes
        self.anime_id = anime_id
    
    def set_seen(self, lo: Loader, seen: bool):
        return lo.post("https://anicloud.io/ajax/watchseason",
                       urlencode({
                           "series": self.anime_id,
                           "season": self.season_number,
                           "watch":  seen
                       })).json()["status"]
    
    def __str__(self):
        return f"S{self.season_number} ({len(self.episodes)} Episodes)"
