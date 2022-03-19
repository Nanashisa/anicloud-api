import datetime
from urllib.parse import urlencode

from anicloud.exception import AuthenticationException
from anicloud.networking.load import Loader
from anicloud.util.emoji_parser import parse_emojis


class ShoutboxMessage:
    def __init__(self, msg_id: int, timestamp: datetime.datetime, content: str, user_id: int,
                 username: str, picture: str, rank: str):
        self.rank = rank
        self.picture = "/public/img/profil/" + picture
        self.username = username
        self.user_id = user_id
        self.content = parse_emojis(content)
        self.timestamp = timestamp
        self.msg_id = msg_id
    
    def __str__(self):
        return f"{self.username}: \"{self.content}\""


class Shoutbox:
    def __init__(self, lo: Loader):
        if not lo.authed:
            raise AuthenticationException()
        self.loader = lo
        self.messages: list[ShoutboxMessage] = []
    
    def update_messages(self) -> tuple[list[ShoutboxMessage], list[int]]:
        data = {"last": self.messages[-1].msg_id} if len(self.messages) > 0 else {}
        req = self.loader.post("https://anicloud.io/ajax/getLastPost", urlencode(data))
        if req.status_code == 200:
            ret1: list[ShoutboxMessage] = []
            ret2: list[int] = req.json()["hideposts"]
            if req.json()["status"]:
                for message in req.json()["posts"]:
                    msg = ShoutboxMessage(
                            message["id"],
                            datetime.datetime.fromtimestamp(int(message["timeago"])),
                            message["message"],
                            message["userID"],
                            message["username"],
                            message["picture"],
                            message["rank"]
                    )
                    print(message["message"])
                    self.messages.append(msg)
                    ret1.append(msg)
            self.messages = [e for e in self.messages if e.msg_id not in ret2]
            return ret1, ret2
        return [], []
    
    def create_post(self, s: str):
        req = self.loader.post("https://anicloud.io/ajax/createShoutboxPost", urlencode({"message": s}))
        if req.status_code == 200:
            return req.json()["status"][0]
        return False
