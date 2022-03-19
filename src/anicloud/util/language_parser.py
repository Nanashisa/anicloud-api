from anicloud.data.anidata.hoster import Language


def parse_lang(s: str) -> Language:
    return {"german":           Language.GERMAN,
            "japanese-german":  Language.GERMAN_SUB,
            "japanese-english": Language.ENGLISH_SUB}[s]
