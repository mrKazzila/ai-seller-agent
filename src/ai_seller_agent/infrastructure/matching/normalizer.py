import re
import unicodedata

SPACE_PATTERN = re.compile(r"\s+")
NON_WORD_PATTERN = re.compile(r"[^\w\s./+-]")
DIMENSION_SEPARATOR_PATTERN = re.compile(
    r"(?<=\d)\s*(?:х|x|×|на)\s*(?=\d)",
)
TOOTH_DIMENSION_PATTERN = re.compile(
    r"(?P<diameter>\d+(?:\.\d+)?)\s+на\s+"
    r"(?P<count>\d+)\s*(?P<label>зуб\w*)",
)
THICKNESS_PATTERN = re.compile(
    r"(?P<size>\d+(?:\.\d+)?\s*[хx×]\s*\d+(?:\.\d+)?)"
    r"\s+(?:стенка|стенкой)\s+(?P<thickness>\d+(?:\.\d+)?)",
)
STANDALONE_DIAMETER_PATTERN = re.compile(
    r"\bна\s+(?P<diameter>\d+(?:\.\d+)?)\b",
)
CYRILLIC_GRIT_PATTERN = re.compile(r"\bр(?=\d+\b)")
REQUEST_WORD_PATTERN = re.compile(
    r"\b(?:здравствуйте|привет|пожалуйста|есть|нужен|нужна|нужны|"
    r"нужно|дайте|сколько|какая|какие|подскажите|в\s+наличии)\b",
)
COMPARISON_PATTERN = re.compile(
    r"\bкак\s+у\s+\w+[\W_]+(?:только\s+)?дешевле\b",
)


ALIASES = {
    "болгарка": "ушм",
    "шурик": "шуруповерт",
    "проф труба": "труба профильная",
    "пластиковые хомуты": "стяжка нейлоновая",
    "хомуты пластиковые": "стяжка нейлоновая",
    "наждачка": "шкурка шлифовальная",
    "круг зачистной": "диск шлифовальный зачистной",
    "сдс": "sds",
    "гкл": "гипсокартон",
    "пачка": "уп",
    "метровая": "1000 мм",
    "гайки": "гайка",
    "дюбелей": "дюбель",
    "полтора": "1.5",
}


class TextNormalizer:
    def normalize(self, value: str) -> str:
        value = unicodedata.normalize("NFKC", value)
        value = value.casefold().replace("ё", "е")
        value = value.replace(",", ".")

        for source, target in ALIASES.items():
            value = re.sub(
                rf"\b{re.escape(source)}\b",
                target,
                value,
            )

        value = re.sub(r"\bлс\b", "ls", value)
        value = CYRILLIC_GRIT_PATTERN.sub("p", value)
        value = COMPARISON_PATTERN.sub(" ", value)
        value = TOOTH_DIMENSION_PATTERN.sub(
            r"\g<diameter> мм \g<count> \g<label>",
            value,
        )
        value = THICKNESS_PATTERN.sub(
            r"\g<size>х\g<thickness>",
            value,
        )
        value = DIMENSION_SEPARATOR_PATTERN.sub("х", value)
        value = STANDALONE_DIAMETER_PATTERN.sub(
            r"\g<diameter> мм",
            value,
        )
        value = REQUEST_WORD_PATTERN.sub(" ", value)
        value = NON_WORD_PATTERN.sub(" ", value)
        value = SPACE_PATTERN.sub(" ", value)

        return value.strip()
