from application.use_cases import compute_stats, analyze_text
from domain.interfaces import LanguageDetector, SentimentAnalyzer
from infrastructure.flesch_calculators import flesch_index, flesch_kincaid, interpret_flesch
from infrastructure.language_detector import detect_language
from infrastructure.syllable_counters import get_syllable_counter


def main() -> None:
  text = "Это достаточно длинный русский текст для проверки программы. Он содержит несколько предложений, разные слова и знаки препинания! Программа должна определить русский язык и посчитать слоги."

  try:
    language = detect_language(text)
    counter = get_syllable_counter(language)

    stats = compute_stats(
      text=text,
      syllable_counter=counter,
    )

    flesch = flesch_index(stats, language)
    interpret = interpret_flesch(stats, language)

    try:
      flesch_kin = flesch_kincaid(stats, language)
    except ValueError as error:
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

  except ValueError as error:
    print(f"Error: {error}")


if __name__ == "__main__":
    main()