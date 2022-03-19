import re

from bs4 import BeautifulSoup


def parse_emoji_url(s: str):
    return {"20": "*play*",
            "8":  "<3",
            "9":  ":P",
            "11": ":D",
            "12": "xD",
            "13": "=D",
            "19": "*nerdy*",
            "15": "*cry*",
            "17": ":(",
            "16": "*sleep*",
            "34": "*rolling-eyes*",
            "4":  "*watch*",
            "3":  "*popcorn*",
            "14": "*kiss*",
            "31": "*smiling*",
            "35": "*thinking*",
            "6":  ":thumbsup:",
            "7":  ":thumbsdown:",
            "33": "*pizza*",
            "10": "*party*",
            "32": "*folded-hands*",
            "37": "*hot*"}[re.search(r"(?<=/public/img/smileys/).+(?=.svg)", s).group()]


def parse_emojis(s: str):
    msg = BeautifulSoup(s, features="html.parser")
    for emoji in msg.select("img[src$=\".svg\"]"):
        emoji.insert_after(msg.new_string(parse_emoji_url(emoji.attrs["src"])))
        emoji.unwrap()
    return str(msg)
