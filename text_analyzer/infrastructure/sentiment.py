from textblob import TextBlob
from domain.types import Polarity, Language
from functools import lru_cache
from deep_translator import MyMemoryTranslator
from infrastructure.language_detector import detectLanguage

LANG_CODES = {
    Language.RU: "ru-RU",
    Language.DE: "de-DE",
    Language.FR: "fr-FR",
    Language.EN: "en-GB",
}

@lru_cache(maxsize=None)
def translateToEnglish(text: str) -> str:
  source_lang = detectLanguage(text)
  if source_lang == Language.EN:
    return text
  translator = MyMemoryTranslator(source = LANG_CODES[source_lang], target='en-GB')
  return translator.translate(text)

def analyzeSentimentTextblob(text: str) -> tuple[Polarity, float]:
  translatedText = translateToEnglish(text)
  print(translatedText)
  blob = TextBlob(translatedText)
  polarity = blob.sentiment.polarity
  subjectivity = blob.sentiment.subjectivity

  if polarity > 0.1:
    p = Polarity.POSITIVE
  elif polarity < -0.1:
    p = Polarity.NEGATIVE
  elif -0.1 <= polarity <= 0.1:
    p = Polarity.NEUTRAL
  return p, subjectivity