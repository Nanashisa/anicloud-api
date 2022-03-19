import random


def rnd_ua() -> str:
    uas = [
        {
            "desc": "Firefox 31.0 (Win XP)",
            "ua":   "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0"
        },
        {
            "desc": "Firefox 35.0 (Win 7 64 bit)",
            "ua":   "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:35.0) Gecko/20100101 Firefox/35.0"
        },
        {
            "desc": "Firefox 36.0 (Win 8.1 32 bit)",
            "ua":   "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
        },
        {
            "desc": "Firefox 39.0 (Win 8.0 64 bit)",
            "ua":   "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0"
        },
        {
            "desc": "Firefox 40.0 (Win Vista)",
            "ua":   "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
        },
        {
            "desc": "Firefox 40.0 (Win 10)",
            "ua":   "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
        },
        {
            "desc": "Firefox 47.0 (Win 10)",
            "ua":   "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
        },
        {
            "desc": "Firefox 52.0 (Win 10)",
            "ua":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"
        },
        {
            "desc": "Firefox 57.0 (Win 10 64 bit)",
            "ua":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
        },
        {
            "desc": "Firefox 35.0 (OS X 10.9 Intel)",
            "ua":   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:35.0) Gecko/20100101 Firefox/35.0"
        },
        {
            "desc": "Firefox 40.0 (OS X 10.10 Intel)",
            "ua":   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0"
        },
        {
            "desc": "Firefox 47.0 (OS X 10.9 Intel)",
            "ua":   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:47.0) Gecko/20100101 Firefox/47.0"
        },
        {
            "desc": "Firefox 49.0 (OS X 10.12 Intel)",
            "ua":   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"
        },
        {
            "desc": "Firefox 55.0 (OS X 10.13 Intel)",
            "ua":   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"
        },
        {
            "desc": "Firefox 32.0 (32 bit)",
            "ua":   "Mozilla/5.0 (X11; Linux i686; rv:32.0) Gecko/20100101 Firefox/32.0"
        },
        {
            "desc": "Firefox 35.0 (Ubuntu 64 bit)",
            "ua":   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"
        },
        {
            "desc": "Firefox 36.0 (CentOS 64 bit)",
            "ua":   "Mozilla/5.0 (X11; CentOS; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0"
        },
        {
            "desc": "Firefox 38.0 (64 bit)",
            "ua":   "Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"
        },
        {
            "desc": "Firefox 40.0 (32 bit)",
            "ua":   "Mozilla/5.0 (X11; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0"
        },
        {
            "desc": "Firefox 43.0 (32 bit)",
            "ua":   "Mozilla/5.0 (X11; Linux i686; rv:43.0) Gecko/20100101 Firefox/43.0"
        },
        {
            "desc": "Firefox 46.0 (32 bit)",
            "ua":   "Mozilla/5.0 (X11; Linux i686; rv:46.0) Gecko/20100101 Firefox/46.0"
        },
        {
            "desc": "Firefox 49.0 (32 bit)",
            "ua":   "Mozilla/5.0 (X11; Linux i686; rv:49.0) Gecko/20100101 Firefox/49.0"
        },
        {
            "desc": "Firefox 49.0 (Fedora 64 bit)",
            "ua":   "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"
        },
        {
            "desc": "Firefox 49.0 (Ubuntu 64 bit)",
            "ua":   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"
        },
        {
            "desc": "Firefox 55.0 (64 bit)",
            "ua":   "Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0"
        },
        {
            "desc": "Firefox 55.0 (Ubuntu 64 bit)",
            "ua":   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0"
        },
        {
            "desc": "Firebird 0.6 (SunOs)",
            "ua":   "Mozilla/5.0 (X11; U; SunOS sun4m; en-US; rv:1.4b) Gecko/20030517 Mozilla Firebird/0.6"
        },
        {
            "desc": "Firefox 3.1b3 (SunOs)",
            "ua":   "Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.9.1b3) Gecko/20090429 Firefox/3.1b3"
        },
        {
            "desc": "Firefox 30.0 (NetBSD 64)",
            "ua":   "Mozilla/5.0 (X11; NetBSD amd64; rv:30.0) Gecko/20100101 Firefox/30.0"
        },
        {
            "desc": "Firefox 30.0 (OpenBSD 64)",
            "ua":   "Mozilla/5.0 (X11; OpenBSD amd64; rv:30.0) Gecko/20100101 Firefox/30.0"
        },
        {
            "desc": "Firefox 35.0 (FreeBSD 64)",
            "ua":   "Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 "
                    "Safari/537.36"
        },
        {
            "desc": "Firefox 54.0 (FreeBSD 64)",
            "ua":   "Mozilla/5.0 (X11; FreeBSD amd64; rv:54.0) Gecko/20100101 Firefox/54.0"
        },
        {
            "desc": "Firefox 35.0 - Android",
            "ua":   "Mozilla/5.0 (Android; Mobile; rv:35.0) Gecko/35.0 Firefox/35.0"
        },
        {
            "desc": "Firefox 4.0.1 (Win CE)",
            "ua":   "Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
        },
        {
            "desc": "Firefox Fennec 1.0.a1 (Linux arm)",
            "ua":   "Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1"
        },
        {
            "desc": "Firefox Fennec 2.0.1 (Maemo arm)",
            "ua":   "Mozilla/5.0 (Maemo; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1"
        },
        {
            "desc": "Firefox Fennec 10.0.1 (Maemo arm)",
            "ua":   "Mozilla/5.0 (Maemo; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1"
        },
        {
            "desc": "Firefox 48.0 - Android 6.0.1 (Samsung SM-G935F)",
            "ua":   "Mozilla/5.0 (Android 6.0.1; Mobile; rv:48.0) Gecko/48.0 Firefox/48.0"
        }
    ]
    return uas[random.randrange(0, len(uas))]["ua"]
