from infrastructure.flesch_calculators import fleschIndex, interpretFlesch
from domain.types import Text_Stats, Analysis_Result, Language, Polarity
from domain.interfaces import Syllable_Counter, Sentiment_Analyzer, Language_Detector
from infrastructure.language_detector import detectLanguage
from infrastructure.syllable_counters import splitSentences, splitWords, getSyllableCounter, countSyllablesEn
from infrastructure.sentiment import analyzeSentimentTextblob
from infrastructure.syllable_counters import getSyllableCounter
from functools import lru_cache

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

FLESCHKINCAIDCOEFFICIENTS = (-15.59, 0.39, 11.8)


def fleschKincaid(text: str) -> float:
  stats = computeStats(text, getSyllableCounter(Language.EN))
  base, sentenceFactor, syllableFactor = FLESCHKINCAIDCOEFFICIENTS
  scores = base + sentenceFactor * stats.avgSentenceLength + syllableFactor * stats.avgWordSyllables
  return scores

@lru_cache(maxsize=None)
def analyzeText(text: str,
                 lang_detector: Language_Detector,
                 syllableCounter: Syllable_Counter,
                 sentimentAnalyzer: Sentiment_Analyzer) -> Analysis_Result:

  lang = detectLanguage(text)
  syllable_counter = getSyllableCounter(lang)
  stats = computeStats(text, syllable_counter)
  flesch = fleschIndex(stats, lang)

  flesch_kinc = fleschKincaid(text)
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