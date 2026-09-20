from textblob import TextBlob
from domain.types import Polarity
from functools import lru_cache
from deep_translator import MyMemoryTranslator

translator = MyMemoryTranslator(source='fr-FR', target='en-GB')

@lru_cache(maxsize=None)
def translateToEnglish(text: str) -> str:
    return translator.translate(text)

def analyzeSentimentTextblob(text: str) -> tuple[Polarity, float]:
    translatedText = translateToEnglish(text)
    blob = TextBlob(translatedText)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0.1:
        p = Polarity.POSITIVE
    elif polarity < -0.1:
        p = Polarity.NEGATIVE
    else:
        p = Polarity.NEUTRAL
    return p, subjectivity