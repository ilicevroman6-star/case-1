from infrastructure.flesch_calculators import flesch_index, flesch_kincaid, interpret_flesch
from domain.types import TextStats, AnalysisResult, Language, Polarity
from domain.interfaces import SyllableCounter, SentimentAnalyzer, LanguageDetector
from infrastructure.language_detector import detect_language
from infrastructure.syllable_counters import split_sentences, split_words, get_syllable_counter
from infrastructure.sentiment import analyze_sentiment_textblob

def compute_stats(text: str, syllable_counter: SyllableCounter) -> TextStats:
  sentences = split_sentences(text)
  words = split_words(text)
  total_syllables = sum(syllable_counter(w) for w in words)

  sentence_count = len(sentences)
  word_count = len(words)
  syllable_count = total_syllables

  avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
  avg_word_syllables = syllable_count / word_count if word_count > 0 else 0

  return TextStats(
    sentence_count=sentence_count,
    word_count=word_count,
    syllable_count=syllable_count,
    avg_sentence_length=avg_sentence_length,
    avg_word_syllables=avg_word_syllables,
  )


def analyze_text(text: str,
                 lang_detector: LanguageDetector,
                 syllable_counter: SyllableCounter,
                 sentiment_analyzer: SentimentAnalyzer) -> AnalysisResult:

  lang = lang_detector(text)
  syllable_counter = get_syllable_counter(lang)
  stats = compute_stats(text, syllable_counter)
  flesch = flesch_index(stats, lang)

  try:
    flesch_kinc = flesch_kincaid(stats, lang)
  except ValueError:
    flesch_kinc = None
  interpret = interpret_flesch(stats, lang)

  polar, subj = analyze_sentiment_textblob(text)

  return AnalysisResult(
    language=lang,
    flesch_index=flesch,
    flesch_kincaid=flesch_kinc,
    interpretation=interpret,
    polarity=polar.value,
    subjectivity=subj,
    lexical_diversity=0.0,
    rare_word_density=0.0,
    stats=stats,
  )