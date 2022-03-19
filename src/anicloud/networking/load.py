from urllib.parse import urlencode

import requests

from .user_agent import rnd_ua as agent


class Loader:
    def __init__(self, lo=None):
        if lo is not None:
            self.session = lo.session
            self.ua = lo.ua
            self.authed = lo.authed
        else:
            self.session = requests.session()
            self.ua = agent()
            self.session.headers.update({'User-Agent': self.ua})
            self.authed = False
            self.load("https://anicloud.io/")
    
    def load(self, url, **kwargs):
        ret = self.session.get(url, **kwargs)
        while ret.status_code == 403:
            self.session.headers.update({'User-Agent': agent()})
            ret = self.session.get(url, **kwargs)
        return ret
    
    def post(self, url: str, data: str, content_type: str = "application/x-www-form-urlencoded", **kwargs):
        ret = self.session.post(url, data=data, headers={"Content-Type": content_type}, **kwargs)
        while ret.status_code == 403:
            self.session.headers.update({'User-Agent': agent()})
            ret = self.session.post(url, data=data, headers={"Content-Type": content_type}, **kwargs)
        return ret
    
    def post_raw(self, url: str, **kwargs):
        ret = self.session.post(url, **kwargs)
        while ret.status_code == 403:
            self.session.headers.update({'User-Agent': agent()})
            ret = self.session.post(url, **kwargs)
        return ret
    
    def login(self, email: str, password: str) -> bool:
        if self.authed:
            return False
        req = self.post("https://anicloud.io/login",
                        urlencode({
                            "email":     email,
                            "password":  password,
                            "autoLogin": "on"
                        })
                        )
        if req.status_code == 200 and "Refresh" in req.headers:
            self.authed = True
            return True
        return False
    
    def logout(self):
        if self.load("https://anicloud.io/home/logout").status_code == 200:
            self.authed = False
            return True
        return False
    
    def validate_username(self, s: str) -> bool:
        return self.post("https://anicloud.io/ajax/validateUsername", urlencode({"username": s}),
                         content_type="application/x-www-form-urlencoded; charset=UTF-8").json()["status"]
