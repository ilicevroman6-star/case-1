from domain.types import Language, Text_Stats

FLESCHCOEFFICIENTS: dict[Language, tuple[float,float,float]] = {
  Language.EN: (206.835, 1.015, 84.6),
  Language.RU: (206.835, 1.3, 60.1),
  Language.FR: (207, 1.015, 73.6),
  Language.DE: (180, 1.0, 58.5)
}

def fleschIndex(stats: Text_Stats, lang: Language) -> float:
  """
  calculates the flesch-index value of a given text and lang
  :param stats: statistics returned by analyze_text
  :param lang: language
  :return: flesch-index
  90...100 - easy
  60...89 - medium
  30...59 - hard
  0...30 - very hard
  """

  if stats.wordCount == 0 or stats.sentenceCount == 0:
    return 0

  try:
    base, sentenceFactor, syllableFactor = FLESCHCOEFFICIENTS[lang]
  except KeyError as error:
      raise ValueError('Unknown language') from error

  score = base - sentenceFactor * stats.avgSentenceLength - syllableFactor * stats.avgWordSyllables

  return score

FLESCHKINCAIDCOEFFICIENTS: dict[Language, tuple[float,float,float]] = {
  Language.EN: (-15.59, 0.39, 11.8)
}

def fleschKincaid(stats: Text_Stats, lang: Language) -> float:
  if stats.wordCount == 0 or stats.sentenceCount == 0:
    return 0

  try:
    base, sentenceFactor, syllableFactor = FLESCHKINCAIDCOEFFICIENTS[lang]
  except KeyError as error:
    raise ValueError(f"Flesch-Kincaid Grade level if defined only for English language. "
                     f"Unsupposed language: {lang}") from error
  score = sentenceFactor * stats.avgSentenceLength + syllableFactor * stats.avgWordSyllables + base

  return score

def interpretFlesch(score: float, lang: Language) -> str:
  if 90 < fleschIndex(score, lang) < 100:
    return 'Easy'
  elif 60 < fleschIndex(score, lang) < 89:
    return 'Medium'
  elif 30 < fleschIndex(score, lang) < 59:
    return 'Hard'
  else:
    return 'Very hard'