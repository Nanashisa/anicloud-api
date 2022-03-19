from enum import Enum
from urllib.parse import urlencode

from anicloud.data.anidata.account import Account
from anicloud.networking.load import Loader


class FriendshipStatus(Enum):
    SENT = 1
    RECEIVED = 2
    ACTIVE = 3


class Friendship:
    def __init__(self, friendship_id: int, profile: Account, status: FriendshipStatus, lo: Loader):
        self.lo = lo
        self.id = friendship_id
        self.profile = profile
        self.status: FriendshipStatus = status
    
    def accept(self):
        if self.status == FriendshipStatus.SENT:
            return False
        return self.lo.post("https://anicloud.io/ajax/friendshipRequestStatus",
                            urlencode({"requestID": self.id, "status": 1})).json()["status"]
    
    def reject(self):
        if self.status == FriendshipStatus.SENT:
            return False
        return self.lo.post("https://anicloud.io/ajax/friendshipRequestStatus",
                            urlencode({"requestID": self.id, "status": 2})).json()["status"]
    
    def revoke_request(self):
        if self.status == FriendshipStatus.RECEIVED:
            return False
        return self.lo.post("https://anicloud.io/ajax/friendshipRequestStatus",
                            urlencode({"requestID": self.id, "status": 4})).json()["status"]
    
    def cancel(self):
        if self.status != FriendshipStatus.ACTIVE:
            return False
        return self.lo.post("https://anicloud.io/ajax/friendshipRequestStatus",
                            urlencode({"requestID": self.id, "status": 3})).json()["status"]
    
    def __str__(self):
        return str(self.profile) + ": " + self.status.name
