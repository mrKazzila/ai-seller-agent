import re
import unicodedata

SPACE_PATTERN = re.compile(r"\s+")
NON_WORD_PATTERN = re.compile(r"[^\w\s./+-]")
DIMENSION_SEPARATOR_PATTERN = re.compile(
    r"(?<=\d)\s*(?:х|x|×|на)\s*(?=\d)",
)


ALIASES = {
    "болгарка": "ушм",
    "шурик": "шуруповерт",
    "проф труба": "труба профильная",
    "пластиковые хомуты": "стяжка нейлоновая",
    "хомуты пластиковые": "стяжка нейлоновая",
    "наждачка": "шкурка шлифовальная",
    "полтора": "1.5",
}


class TextNormalizer:
    def normalize(self, value: str) -> str:
        value = unicodedata.normalize("NFKC", value)
        value = value.casefold().replace("ё", "е")
        value = value.replace(",", ".")

        for source, target in ALIASES.items():
            value = value.replace(source, target)

        value = DIMENSION_SEPARATOR_PATTERN.sub("х", value)
        value = NON_WORD_PATTERN.sub(" ", value)
        value = SPACE_PATTERN.sub(" ", value)

        return value.strip()
