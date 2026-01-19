import json
from pathlib import Path
from functools import lru_cache
from app.middleware.locale import request_language

BASE_DIR = Path(__file__).resolve().parents[2]
LOCALES_DIR = BASE_DIR / "app" / "locales"


@lru_cache
def load_language(lang: str) -> dict:
    file_path = LOCALES_DIR / f"{lang}.json"

    if not file_path.exists():
        file_path = LOCALES_DIR / "en.json"

    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def translate(key: str, **kwargs) -> str:
    lang = request_language.get()
    translations = load_language(lang)

    text = translations.get(key, key)
    return text.format(**kwargs)
