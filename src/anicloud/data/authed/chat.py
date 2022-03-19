import datetime
import json
from urllib.parse import urlencode
from dateutil.parser import parse as parse_date

from anicloud.data.anidata.account import Account
# from ...networking.load import Loader TODO
from ...util.emoji_parser import parse_emojis


class Message:
    def __init__(self, msg_id: int, username: str, timestamp: datetime.datetime, content: str, seen: bool):
        self.seen = seen
        self.content = parse_emojis(content)
        self.timestamp = timestamp
        self.username = username
        self.msg_id = msg_id
    
    def __str__(self):
        return f"{self.username}: {self.content}"


class Chat:
    def __init__(self, chat_id: int, last_activity: datetime.datetime = None,
                 user: Account = None, last_message: str = None):
        self.chat_id: int = chat_id
        self.last_activity: datetime.datetime = last_activity
        self.user: Account = user
        self.last_message: str = last_message
        self.loaded = False
        self.messages: list[Message] = []
    
    def load(self, lo):  # TODO
        chat = json.loads(lo.post("https://anicloud.io/ajax/getMessages",
                                  data=urlencode({"chatid": self.chat_id})).text)
        self.messages.clear()
        for message in chat["messages"]:
            self.messages.append(Message(message["id"], message["username"],
                                         parse_date(message["timestamp"]), message["message"],
                                         message["display_message"] == "seen"))
            self.last_message = message["message"]
        self.loaded = True
        return True
    
    def new_message(self, text: str, lo):  # TODO
        req = lo.post("https://anicloud.io/ajax/newMessage", urlencode({"chat": self.chat_id, "message": text}))
        return req.json()["status"]
    
    def update_messages(self, lo):  # TODO
        req = lo.post("https://anicloud.io/ajax/getNewMessages",
                      urlencode({"chat": self.chat_id, "last": self.messages[-1].msg_id}))
        for msg in req.json()["messages"]:
            self.messages.append(Message(msg["id"], msg["username"], parse_date(msg["timestamp"]), msg["message"],
                                         msg["display_message"] == "seen"))
            self.last_message = msg["message"]
    
    def __str__(self):
        return self.user
