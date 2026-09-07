from langdetect import language
from textblob import TextBlob
from domain.types import Polarity
from googletrans import Translator
from deep_translator import GoogleTranslator

translator = Translator()

def translateToEnglish(text: str) -> str:
    return GoogleTranslator(source='auto', target='en').translate(text)

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