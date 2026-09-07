import re
from typing import List

from domain.interfaces import Syllable_Counter
from domain.types import Language

def splitSentences(text: str) -> List[str]:
  return [
    sentence.strip()
    for sentence in re.split(r"[.!?…]+", text)
    if sentence.strip()
    ]

def splitWords(sentence: str) -> List[str]:
  return re.findall(r"[^\W\d_]+", sentence, flags=re.UNICODE)

def lettersOnly(word: str) -> str:
  """
  :return:
  removes everything except letters
  :param word: word
  :return: string without digits or special characters
  """
  return "".join(char for char in word.lower() if char.isalpha())

def countSyllablesRu(word: str) -> int:
  """
  counting syllables russian
  :param word: word
  :return: count of syllables
  """
  normalized = lettersOnly(word)
  if not normalized:
    return 0

  vowels = "аеёиоуыэюя"
  return sum(char in vowels for char in normalized)

def countSyllablesEn(word: str) -> int:
  """
  counting syllables english
  :param word: word
  :return: count of syllables
  """
  normalized = lettersOnly(word)
  if not normalized:
    return 0

  vowels = "aeiouy"
  groups = re.findall(r"[aeiouy]+", normalized)
  syllables = len(groups)

  if (
    normalized.endswith(("le", "ye"))
    and syllables > 1
  ):
    syllables -= 1

  if (
    normalized.endswith("ed")
    and len(normalized) > 3
    and syllables > 1
    and not normalized.endswith(("ted", "ded"))
  ):
    syllables -= 1

  return max(1, syllables)

def countSyllablesDe(word: str) -> int:
  """
  counting syllables in german
  :param word: word
  :return: count of syllables
  """
  normalized = lettersOnly(word)

  if not normalized:
    return 0

  groups = re.findall(r"[aeiouyäöü]+", normalized)
  return max(1, len(groups))

def countSyllablesFr(word: str) -> int:
  """
  counting syllables in french
  :param word: word
  :return: count of syllables
  """
  normalized = lettersOnly(word)

  if not normalized:
    return 0

  normalized = normalized.replace("qu", "q")

  groups = re.findall(r"[aeiouyàâäæçèéêëîïôœùûü]+", normalized)
  syllables = len(groups)

  if normalized.endswith(("es", "e")) and syllables > 1:
      syllables -= 1

  return max(1, syllables)

def getSyllableCounter(lang: Language) -> Syllable_Counter:
  """
  get syllable count
  :param lang: language
  :return: syllable count
  """
  counters: dict[Language, Syllable_Counter] = {
    Language.EN : countSyllablesEn,
    Language.RU : countSyllablesRu,
    Language.DE : countSyllablesDe,
    Language.FR : countSyllablesFr,
  }

  try:
    return counters[lang]
  except KeyError as error:
      raise ValueError('Cannot get syllable counter from language') from error