import re
import time
from threading import Lock

from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire.request import Request, Response
from seleniumwire import webdriver


class HostResolver(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument("--app=https://anicloud.io")
        options.add_argument("--disable-notifications")
        super().__init__(executable_path=ChromeDriverManager().install(), chrome_options=options, *args, **kwargs)
        
        def interceptor(request: Request, response: Response):
            if re.match(rf"https?://anicloud.io/redirect/{self.id}\?token=[^&]+&original=",
                        request.url, re.RegexFlag.IGNORECASE):
                self.url = response.headers["location"]
                request.abort(204)
        self.id: int = 0
        self.response_interceptor = interceptor
        self.lock = Lock()
        self.url: str = ""
    
    def resolve(self, link_id: int):
        try:
            with self.lock:
                self.id = link_id
                self.url = ""
                self.get("https://anicloud.io/redirect/" + str(link_id))
                while self.url == "":
                    time.sleep(0.5)
                return self.url
        except WebDriverException:
            return None
        
