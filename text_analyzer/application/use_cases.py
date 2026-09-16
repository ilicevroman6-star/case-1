from domain.interfaces import Language_Detector, Sentiment_Analyzer, Syllable_Counter
from domain.types import Analysis_Result, Language, Polarity, Text_Stats
from infrastructure.flesch_calculators import fleschIndex, fleschKincaid, interpretFlesch
from infrastructure.language_detector import detectLanguage
from infrastructure.sentiment import analyzeSentimentTextblob
from infrastructure.syllable_counters import getSyllableCounter, splitSentences, splitWords


def computeStats(text: str, syllableCounter: Syllable_Counter) -> Text_Stats:
  sentences = splitSentences(text)
  words = splitWords(text)
  totalSyllables = sum(syllableCounter(w) for w in words)

  sentenceCount = len(sentences)
  wordCount = len(words)
  syllableCount = totalSyllables

  avgSentenceLength = wordCount / sentenceCount if sentenceCount > 0 else 0
  avgWordSyllables = syllableCount / wordCount if wordCount > 0 else 0

  return Text_Stats(
    sentenceCount=sentenceCount,
    wordCount=wordCount,
    syllableCount=syllableCount,
    avgSentenceLength=avgSentenceLength,
    avgWordSyllables=avgWordSyllables,
  )


def analyzeText(text: str,
                 lang_detector: Language_Detector,
                 syllableCounter: Syllable_Counter,
                 sentimentAnalyzer: Sentiment_Analyzer) -> Analysis_Result:

  lang = lang_detector(text)
  syllable_counter = getSyllableCounter(lang)
  stats = computeStats(text, syllable_counter)
  flesch = fleschIndex(stats, lang)

  try:
    flesch_kinc = fleschKincaid(stats, lang)
  except ValueError:
    flesch_kinc = None
  interpret = interpretFlesch(stats, lang)

  polar, subj = analyzeSentimentTextblob(text)

  return Analysis_Result(
    language=lang,
    fleschIndex=flesch,
    fleschKincaid=flesch_kinc,
    interpretation=interpret,
    polarity=polar.value,
    subjectivity=subj,
    lexicalDiversity=0.0,
    rareWordDensity=0.0,
    stats=stats,
  )


def analyzeBatch(texts: list[str], **deps) -> list[Analysis_Result]:
  return [analyzeText(t, **deps) for t in texts]
