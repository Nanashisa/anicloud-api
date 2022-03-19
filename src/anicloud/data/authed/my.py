import json
from datetime import datetime
from enum import Enum
from io import BytesIO
from urllib.parse import urlencode
from dateutil.parser import parse as parse_date

from bs4 import BeautifulSoup

from anicloud.data.anidata.account import Account
from anicloud.data.authed.chat import Chat
from anicloud.data.authed.friendship import Friendship, FriendshipStatus
from anicloud.exception import AuthenticationException
from anicloud.networking.load import Loader
from anicloud.util.button_in_text import parse_url_button_in_text
from anicloud.util.real_url import real_url


class NotificationColor(Enum):
    """
    Color of the icon-background of live-notifications
    """
    red = "red"
    blue = "blue"
    green = "green"
    yellow = "yellow"
    orange = "orange"
    grey = "grey"
    turquoise = "turquoise"
    purple = "purple"
    black = "black"


class Notification:
    """
    Notification, either live or from the inbox
    """
    def __init__(self, isLive: bool, message: str, icon: str, url: str = None, timestamp: datetime = None,
                 color: NotificationColor = None, notif_id: int = None):
        """
        Notification, either live or from the inbox
        :param isLive: Whether the notification comes from the live notification API-backend
        :param message: Notification's text
        :param icon: Notification's icon, use in AwesomeFontIconParser
        :param url: (Optional) Url to where the notification navigates on click
        :param timestamp: (Optional) When the notification was sent
        :param color: What color the notification has
        :param notif_id: The notification's identifier
        """
        self.icon = icon
        self.timestamp = timestamp
        self.message = message
        self.url = url
        self.color = color
        self.isLive = isLive
        self.id = notif_id


class MyAccount:
    """
    Manage changes in settings and account specific functions
    """
    def __init__(self, lo: Loader):
        """
        Manage changes in settings and account specific functions
        :param lo: Authorized Loader instance
        """
        if not lo.authed:
            raise AuthenticationException
        self.lo = lo
    
    def settings(self,
                 userDescription: str = None,
                 place: str = None,
                 website: str = None,
                 password: str = "",
                 username: str = None,
                 themeStyle: bool = None,
                 emailNotifications: bool = None,
                 newsletter: bool = None,
                 notificationSound: bool = None,
                 homepageAnimation: bool = None,
                 emailNotificationEpisodeLanguageGerman: bool = None,
                 emailNotificationEpisodeLanguageGermanSubtitle: bool = None,
                 emailNotificationEpisodeLanguageEnglishSubtitle: bool = None,
                 publicProfile: bool = None,
                 socialMedia: bool = None,
                 statistics: bool = None) -> bool:
        """

        :param userDescription: Description displayed on the right of the user's profile page
        :param place: (Optional) User's location
        :param website: (Optional) User's private website (maybe broken, can't change)
        :param password: User's password, repetition for verification to be made by the developer
        :param username: User's account name
        :param themeStyle: Whether to use light theme
        :param emailNotifications: Whether to send notifications via e-mail
        :param newsletter: Whether to send the user monthly notifications about current changes
        :param notificationSound: Whether to play a sound on new messages in the shoutbox
        :param homepageAnimation: Whether deactivate animations on the homepage (performance)
        :param emailNotificationEpisodeLanguageGerman: Whether to inform about new german episodes
        :param emailNotificationEpisodeLanguageGermanSubtitle: Whether to inform about new german subbed episodes
        :param emailNotificationEpisodeLanguageEnglishSubtitle: Whether to inform about new english subbed episodes
        :param publicProfile: Whether to show the user's profile page publicly
        :param socialMedia: Whether to show embed social media buttons
        :param statistics: Whether to allow anonymous statistics by anicloud.io
        :return: Success
        """
        provided_data = BeautifulSoup(self.lo.load("https://anicloud.io/account/settings").text, features="html.parser")
        if userDescription is None:
            userDescription = provided_data.select_one("form textarea[name=\"userDescription\"]").text
        if place is None:
            place = provided_data.select_one("form input[name=\"place\"]").attrs["value"]
        if website is None:
            website = provided_data.select_one("form input[name=\"website\"]").attrs["value"]
        if username is None:
            username = provided_data.select_one("form input[name=\"username\"]").attrs["value"]
        if themeStyle is None:
            themeStyle = provided_data.select_one("form input[name=\"themeStyle\"]").has_attr("checked")
        if emailNotifications is None:
            emailNotifications = provided_data.select_one("form input[name=\"emailNotifications\"]").has_attr("checked")
        if newsletter is None:
            newsletter = provided_data.select_one("form input[name=\"newsletter\"]").has_attr("checked")
        if notificationSound is None:
            notificationSound = provided_data.select_one("form input[name=\"notificationSound\"]").has_attr("checked")
        if homepageAnimation is None:
            homepageAnimation = provided_data.select_one("form input[name=\"homepageAnimation\"]").has_attr("checked")
        if emailNotificationEpisodeLanguageGerman is None:
            emailNotificationEpisodeLanguageGerman = provided_data.select_one(
                    "form input[name=\"emailNotificationEpisodeLanguageGerman\"]").has_attr("checked")
        if emailNotificationEpisodeLanguageGermanSubtitle is None:
            emailNotificationEpisodeLanguageGermanSubtitle = provided_data.select_one(
                    "form input[name=\"emailNotificationEpisodeLanguageGermanSubtitle\"]").has_attr("checked")
        if emailNotificationEpisodeLanguageEnglishSubtitle is None:
            emailNotificationEpisodeLanguageEnglishSubtitle = provided_data.select_one(
                    "form input[name=\"emailNotificationEpisodeLanguageEnglishSubtitle\"]").has_attr("checked")
        if publicProfile is None:
            publicProfile = provided_data.select_one("form input[name=\"publicProfile\"]").has_attr("checked")
        if socialMedia is None:
            socialMedia = provided_data.select_one("form input[name=\"socialMedia\"]").has_attr("checked")
        if statistics is None:
            statistics = provided_data.select_one("form input[name=\"statistics\"]").has_attr("checked")
        if len(place) > 100 or len(userDescription) > 150 or len(username) > 20 or len(password) > 40:
            return False
        data = {
            "userDescription": userDescription,
            "place":           place,
            "website":         website,
            "password1":       password,
            "password2":       password,
            "username":        username
        }
        if themeStyle:
            data["themeStyle"] = "on"
        if themeStyle:
            data["themeStyle"] = "on"
        if emailNotifications:
            data["emailNotifications"] = "on"
        if newsletter:
            data["newsletter"] = "on"
        if notificationSound:
            data["notificationSound"] = "on"
        if homepageAnimation:
            data["homepageAnimation"] = "on"
        if emailNotificationEpisodeLanguageGerman:
            data["emailNotificationEpisodeLanguageGerman"] = "on"
        if emailNotificationEpisodeLanguageGermanSubtitle:
            data["emailNotificationEpisodeLanguageGermanSubtitle"] = "on"
        if emailNotificationEpisodeLanguageEnglishSubtitle:
            data["emailNotificationEpisodeLanguageEnglishSubtitle"] = "on"
        if publicProfile:
            data["publicProfile"] = "on"
        if socialMedia:
            data["socialMedia"] = "on"
        if statistics:
            data["statistics"] = "on"
        return self.lo.post("https://anicloud.io/account/settings", urlencode(data)).status_code == 200
    
    def gettings(self):
        """
        Get all current account-settings
        :return: Dictionary of all settings by name
        """
        provided_data = BeautifulSoup(self.lo.load("https://anicloud.io/account/settings").text, features="html.parser")
        return {
            "userDescription":
                provided_data.select_one("form textarea[name=\"userDescription\"]").text,
            "place":
                provided_data.select_one("form input[name=\"place\"]").attrs["value"],
            "website":
                provided_data.select_one("form input[name=\"website\"]").attrs["value"],
            "username":
                provided_data.select_one("form input[name=\"username\"]").attrs["value"],
            "themeStyle":
                provided_data.select_one("form input[name=\"themeStyle\"]").has_attr("checked"),
            "emailNotifications":
                provided_data.select_one("form input[name=\"emailNotifications\"]").has_attr("checked"),
            "newsletter":
                provided_data.select_one("form input[name=\"newsletter\"]").has_attr("checked"),
            "notificationSound":
                provided_data.select_one("form input[name=\"notificationSound\"]").has_attr("checked"),
            "homepageAnimation":
                provided_data.select_one("form input[name=\"homepageAnimation\"]").has_attr("checked"),
            "emailNotificationEpisodeLanguageGerman":
                provided_data.select_one(
                        "form input[name=\"emailNotificationEpisodeLanguageGerman\"]").has_attr("checked"),
            "emailNotificationEpisodeLanguageGermanSubtitle":
                provided_data.select_one(
                        "form input[name=\"emailNotificationEpisodeLanguageGermanSubtitle\"]").has_attr("checked"),
            "emailNotificationEpisodeLanguageEnglishSubtitle":
                provided_data.select_one(
                        "form input[name=\"emailNotificationEpisodeLanguageEnglishSubtitle\"]").has_attr("checked"),
            "publicProfile":
                provided_data.select_one("form input[name=\"publicProfile\"]").has_attr("checked"),
            "socialMedia":
                provided_data.select_one("form input[name=\"socialMedia\"]").has_attr("checked"),
            "statistics":
                provided_data.select_one("form input[name=\"statistics\"]").has_attr("checked")
        }
    
    def set_profile_picture(self, img: bytes, ext: str):
        """
        Overwrite the profile-picture displayed in the profile-page's foreground
        :param img: Byte-data of the image file to upload
        :param ext: extension  of the image-byte's format (e.g. jpg, png, etc.)
        :return: Success
        """
        img_bytes = BytesIO(img)
        if img_bytes.getbuffer().nbytes > 1024 ** 2:
            return False
        req = self.lo.post_raw("https://anicloud.io/account/settings/profile-picture",
                               files={'userfile': ('image.' + ext, BytesIO(img))})
        return req.status_code == 200
    
    def set_profile_background(self, img: bytes, ext: str):
        """
        Overwrite the picture displayed in the profile-page's background
        :param img: Byte-data of the image file to upload
        :param ext: extension  of the image-byte's format (e.g. jpg, png, etc.)
        :return: Success
        """
        img_bytes = BytesIO(img)
        if img_bytes.getbuffer().nbytes > 1024 ** 2:
            return False
        req = self.lo.post_raw("https://anicloud.io/account/settings/profile-background",
                               files={'userfile': ('image.' + ext, BytesIO(img))})
        return req.status_code == 200
    
    def clear_sessions(self):
        """
        Remove authorization of all session except the current one
        :return: Success
        """
        return self.lo.load("https://anicloud.io/account/clear-sessions").status_code == 200
    
    def chats(self):
        """
        Get instances of all the user's active chats
        :return: List of all chats, id of last used chat
        """
        initChat = json.loads(self.lo.post("https://anicloud.io/ajax/initChat", data=urlencode({"status": 1})).text)
        chats = [Chat(chat["id"], datetime.fromtimestamp(chat["timestamp"]), chat["user"][0]["username"],
                      chat["message"])
                 for chat in initChat["chats"]]
        lastChatId = initChat["lastChatID"]
        return chats, lastChatId
    
    def get_friendships(self):
        """
        Get all friendships and friendship requests
        :return: List of requests and friendships
        """
        html = BeautifulSoup(self.lo.load("https://anicloud.io/account/friendships").text, features="html.parser")
        ret = []
        for friendship in html.select("#friends ul li[data-friendship-id]"):
            ret.append(Friendship(friendship.attrs["data-friendship-id"],
                                  Account(friendship.select_one("a").attrs["href"].strip("/").split("/")[-1],
                                          friendship.select_one("h3").text.strip()),
                                  FriendshipStatus.ACTIVE,
                                  self.lo))
        for request in html.select("#friendshiprequests ul li[data-friendship-id]"):
            ret.append(Friendship(request.attrs["data-friendship-id"],
                                  Account(request.select_one("a").attrs["href"].strip("/").split("/")[-1],
                                          request.select_one("h3").text.strip()),
                                  FriendshipStatus.RECEIVED if
                                  len(request.select("div[data-requestStatus]")) > 1
                                  else FriendshipStatus.SENT,
                                  self.lo))
        return ret
    
    def recent_notifications(self, last_timestamp: datetime):
        """
        Get the latest Notifications
        :param last_timestamp: DateTime, of last received notification
        :return: Count of unread notifications, List of new notifications, Timestamp for next call
        """
        data = self.lo.post("https://anicloud.io/ajax/notifications",
                            urlencode({"lastTimestamp": int(last_timestamp.timestamp())}))
        return int(data["count"]), [
            Notification(False, notif["message"], notif["icon"], real_url(notif["url"]), parse_date(notif["timestamp"]))
            for notif in data["notifications"]
        ], datetime.fromtimestamp(data["timestamp"])
    
    def live_notifications(self):
        """
        Get Live-Notifications
        :return: List of Notifications
        """
        data = self.lo.post("https://anicloud.io/ajax/checkLiveNotifications", urlencode({"live": True})).json()
        ret = []
        for notif in data:
            text, dat = parse_url_button_in_text(notif["message"])
            url = real_url(dat[0][0]) if len(dat) > 0 else None
            ret.append(Notification(True, text, notif["icon"], url,
                                    color=NotificationColor(notif["color"]),
                                    notif_id=notif["id"]))
        return ret
