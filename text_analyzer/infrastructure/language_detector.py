from langdetect import detect, LangDetectException, DetectorFactory

from domain.types import Language

DetectorFactory.seed = 0

MAPPING = {
    "en": Language.EN,
    "ru": Language.RU,
    "de": Language.DE,
    "fr": Language.FR,
}
def detectLanguage(text: str) -> Language:
  """
  It detects the language of the text using the langdetect library.
  :param text: text to be analyzed
  :return: language of the text
  Raises:
    ValueError: if the language cannot be detected, text is too short or empty
  """
  if not text or not text.strip():
    raise ValueError('Cannot detect language')

  try:
    detectedLanguage = detect(text)
  except LangDetectException as error:
    raise ValueError('Cannot detect language') from error

  try:
    return MAPPING[detectedLanguage]
  except KeyError as error:
      raise ValueError('Detected language is not supported') from error