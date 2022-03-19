from bs4 import BeautifulSoup


def parse_url_button_in_text(s: str):
    html = BeautifulSoup(s, features="html.parser")
    data = []
    for a in html.select("a"):
        data.append((a.attrs["href"], a.text.strip()))
        a.replace_with("")
    return html.text.strip(), data
