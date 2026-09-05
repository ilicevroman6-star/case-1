import asyncio

from langdetect import language
from textblob import TextBlob
from domain.types import Polarity
from googletrans import Translator

translator = Translator()

async def translate_to_english(text: str) -> str:
    async with Translator() as translator:
        translated = await translator.translate(text, dest="en")
    return translated.text

def analyze_sentiment_textblob(text: str) -> tuple[Polarity, float]:
    translated_text = asyncio.run(translate_to_english(text))
    blob = TextBlob(translated_text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0.1:
        p = Polarity.POSITIVE
    elif polarity < -0.1:
        p = Polarity.NEGATIVE
    else:
        p = Polarity.NEUTRAL
    return p, subjectivity