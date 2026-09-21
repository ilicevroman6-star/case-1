from infrastructure.flesch_calculators import fleschIndex, interpretFlesch
from domain.types import Text_Stats, Analysis_Result, Language, Polarity
from domain.interfaces import Syllable_Counter, Sentiment_Analyzer, Language_Detector
from infrastructure.language_detector import detectLanguage
from infrastructure.syllable_counters import splitSentences, splitWords, getSyllableCounter, countSyllablesEn
from infrastructure.sentiment import analyzeSentimentTextblob, translateToEnglish
from infrastructure.syllable_counters import getSyllableCounter
from infrastructure.additional_metrics import lexicalDiversity, rareWordDensity
from collections import Counter

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

maxsize=None
def analyzeText(text: str,
                 lang_detector=detectLanguage,
                 syllableCounter=getSyllableCounter,
                 sentimentAnalyzer=Sentiment_Analyzer) -> Analysis_Result:

  lang = lang_detector(text)
  lang = detectLanguage(text)
  syllable_counter = getSyllableCounter(lang)
  stats = computeStats(text, syllable_counter)
  flesch = fleschIndex(stats, lang)

  try:
    flesch_kinc = fleschKincaid(translateToEnglish(text))
  except ValueError:
    flesch_kinc = None
  interpret = interpretFlesch(stats, lang)
  lexical_div = lexicalDiversity(text)
  rare = rareWordDensity(text, freqDict=Counter(text))
  polar, subj = analyzeSentimentTextblob(text)

  return Analysis_Result(
    language=lang,
    fleschIndex=flesch,
    fleschKincaid=flesch_kinc,
    interpretation=interpret,
    polarity=polar.value,
    subjectivity=subj,
    lexicalDiversity=lexical_div,
    rareWordDensity=rare,
    stats=stats,
  )

def analyzeBatch(texts: list[str], **deps) -> list[Analysis_Result]:
  return [analyzeText(t, **deps) for t in texts]