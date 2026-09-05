import re
from typing import List

from domain.interfaces import SyllableCounter
from domain.types import Language

def split_sentences(text: str) -> List[str]:
  return [
    sentence.strip()
    for sentence in re.split(r"[.!?…]+", text)
    if sentence.strip()
    ]

def split_words(sentence: str) -> List[str]:
  return re.findall(r"[^\W\d_]+", sentence, flags=re.UNICODE)

def letters_only(word: str) -> str:
  """
  :return:
  removes everything except letters
  :param word: word
  :return: string without digits or special characters
  """
  return "".join(char for char in word.lower() if char.isalpha())

def count_syllables_ru(word: str) -> int:
  """
  counting syllables russian
  :param word: word
  :return: count of syllables
  """
  normalized = letters_only(word)
  if not normalized:
    return 0

  vowels = "аеёиоуыэюя"
  return sum(char in vowels for char in normalized)

def count_syllables_en(word: str) -> int:
  """
  counting syllables english
  :param word: word
  :return: count of syllables
  """
  normalized = letters_only(word)
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

def count_syllables_de(word: str) -> int:
  """
  counting syllables in german
  :param word: word
  :return: count of syllables
  """
  normalized = letters_only(word)

  if not normalized:
    return 0

  groups = re.findall(r"[aeiouyäöü]+", normalized)
  return max(1, len(groups))

def count_syllables_fr(word: str) -> int:
  """
  counting syllables in french
  :param word: word
  :return: count of syllables
  """
  normalized = letters_only(word)

  if not normalized:
    return 0

  normalized = normalized.replace("qu", "q")

  groups = re.findall(r"[aeiouyàâäæçèéêëîïôœùûü]+", normalized)
  syllables = len(groups)

  if normalized.endswith(("es", "e")) and syllables > 1:
      syllables -= 1

  return max(1, syllables)

def get_syllable_counter(lang: Language) -> SyllableCounter:
  """
  get syllable count
  :param lang: language
  :return: syllable count
  """
  counters: dict[Language, SyllableCounter] = {
    Language.EN : count_syllables_en,
    Language.RU : count_syllables_ru,
    Language.DE : count_syllables_de,
    Language.FR : count_syllables_fr,
  }

  try:
    return counters[lang]
  except KeyError as error:
      raise ValueError('Cannot get syllable counter from language') from error