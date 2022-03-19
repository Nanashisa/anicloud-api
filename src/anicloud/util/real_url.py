def real_url(s: str):
    return s if s.startswith("http") else ("https://anicloud.io" + s)
