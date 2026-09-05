from application.use_cases import compute_stats
from infrastructure.language_detector import detect_language
from infrastructure.syllable_counters import get_syllable_counter

def main() -> None:
  text = ""

  try:
    language = detect_language(text)

    counter = get_syllable_counter(language)

    stats = compute_stats(
      text=text,
      syllable_counter=counter,
    )

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
    print(
      "Average sentence length: "
      f"{stats.avg_sentence_length:.2f} words"
    )
    print(
      "Average syllable count in words: "
      f"{stats.avg_word_syllables:.2f}"
    )

  except ValueError as error:
    print(f"Error: {error}")


if __name__ == "__main__":
    main()