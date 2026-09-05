from domain.types import TextStats, AnalysisResult, Language, Polarity
from domain.interfaces import SyllableCounter, SentimentAnalyzer, LanguageDetector
from infrastructure.syllable_counters import split_sentences, split_words, get_syllable_counter


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

def flesch_index(stats: TextStats, lang: Language) -> float:
  return None

def interpret_flesch(score: float, lang: Language) -> str:
  return None

def analyze_text(text: str,
                 lang_detector: LanguageDetector,
                 sentiment_analyzer: SentimentAnalyzer) -> AnalysisResult:

  lang = lang_detector(text)
  syllable_counter = get_syllable_counter(lang)

  stats = compute_stats(text, syllable_counter)

  return AnalysisResult(
    language=lang,
    flesch_index=0.0,
    flesch_kincaid=0.0,
    interpretation="Not calculated yet",
    polarity=Polarity.NEUTRAL,
    subjectivity=0.0,
    lexical_diversity=0.0,
    rare_word_density=0.0,
    stats=stats,
  )