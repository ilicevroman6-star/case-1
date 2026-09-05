from application.use_cases import compute_stats, analyze_text
from domain.interfaces import LanguageDetector, SentimentAnalyzer
from infrastructure.flesch_calculators import flesch_index, flesch_kincaid, interpret_flesch
from infrastructure.language_detector import detect_language
from infrastructure.syllable_counters import get_syllable_counter
from infrastructure.sentiment import analyze_sentiment_textblob

def main() -> None:
  text = "Я не могу поверить, что он так со мной поступил. Это просто низко и подло. После всего, что мы пережили, он решил меня предать. Такое ощущение, что у него вообще нет никаких принципов"

  try:
    language = detect_language(text)
    counter = get_syllable_counter(language)

    stats = compute_stats(
      text=text,
      syllable_counter=counter,
    )

    flesch = flesch_index(stats, language)
    interpret = interpret_flesch(stats, language)
    polar, subj = analyze_sentiment_textblob(text)

    try:
      flesch_kin = flesch_kincaid(stats, language)
    except ValueError:
      flesch_kin = None

    if language.value == 1:
      print("Language: English")
    if language.value == 2:
      print("Language: Russian")
    if language.value == 3:
      print("Language: German")
    if language == 4:
      print("Language: French")

    print(f"Count of sentences: {stats.sentence_count}")
    print(f"Count of words: {stats.word_count}")
    print(f"Count of syllables: {stats.syllable_count}")
    print("Average sentence length: "f"{stats.avg_sentence_length:.2f} words")
    print("Average syllable count in words: "f"{stats.avg_word_syllables:.2f}")
    print("Flesch index: "f"{flesch:.2f}")
    if flesch_kin is not None:
      print("Flesch-Kincaid index: "f"{flesch_kin:.2f}")
    else:
      print("Flesch-Kincaid index: unavailable")
    print("Interpret Flesch: "f"{interpret}")
    print("Polarity: "f"{polar.value}")
    print("Subjectivity: "f"{subj}")

  except ValueError as error:
    print(f"Error: {error}")


if __name__ == "__main__":
    main()