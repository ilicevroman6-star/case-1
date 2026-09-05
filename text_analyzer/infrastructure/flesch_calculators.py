from domain.types import Language, TextStats

fleshCoefficients: dict[Language, tuple[float,float,float]] = {
  Language.EN: (206.835, 1.015, 84.6),
  Language.RU: (206.835, 1.3, 60.1),
  Language.FR: (207, 1.015, 73.6),
  Language.DE: (180, 1.0, 58.5)
}

def flesch_index(stats: TextStats, lang: Language) -> float:
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

  if stats.word_count == 0 or stats.sentence_count == 0:
    return 0

  try:
    base, sentence_factor, syllable_factor = fleshCoefficients[lang]
  except KeyError as error:
      raise ValueError('Unknown language') from error

  score = base - sentence_factor * stats.avg_sentence_length - syllable_factor * stats.avg_word_syllables

  return score

fleschKincaidCoefficients: dict[Language, tuple[float,float,float]] = {
  Language.EN: (-15.59, 0.39, 11.8)
}

def flesch_kincaid(stats: TextStats, lang: Language) -> float:
  if stats.word_count == 0 or stats.sentence_count == 0:
    return 0

  try:
    base, sentence_factor, syllable_factor = fleschKincaidCoefficients[lang]
  except KeyError as error:
    raise ValueError(f"Flesch-Kincaid Grade level if defined only for English language. "
                     f"Unsupposed language: {lang}") from error
  score = sentence_factor * stats.avg_sentence_length + syllable_factor * stats.avg_word_syllables + base

  return score

def interpret_flesch(score: float, lang: Language) -> str:
  if 90 < flesch_index(score, lang) < 100:
    return 'Easy'
  elif 60 < flesch_index(score, lang) < 89:
    return 'Medium'
  elif 30 < flesch_index(score, lang) < 59:
    return 'Hard'
  else:
    return 'Very hard'