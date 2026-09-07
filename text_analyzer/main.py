from application.use_cases import computeStats, analyzeText
from domain.interfaces import Language_Detector, Sentiment_Analyzer
from infrastructure.flesch_calculators import fleschIndex, fleschKincaid, interpretFlesch
from infrastructure.language_detector import detectLanguage
from infrastructure.syllable_counters import getSyllableCounter
from infrastructure.sentiment import analyzeSentimentTextblob

def main() -> None:
  text = "Я не могу поверить, что он так со мной поступил. Это просто низко и подло. После всего, что мы пережили, он решил меня предать. Такое ощущение, что у него вообще нет никаких принципов"

  try:
    language = detectLanguage(text)
    counter = getSyllableCounter(language)

    stats = computeStats(
      text=text,
      syllableCounter=counter,
    )

    flesch = fleschIndex(stats, language)
    interpret = interpretFlesch(stats, language)
    polar, subj = analyzeSentimentTextblob(text)

    try:
      flesch_kin = fleschKincaid(stats, language)
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

    print(f"Count of sentences: {stats.sentenceCount}")
    print(f"Count of words: {stats.wordCount}")
    print(f"Count of syllables: {stats.syllableCount}")
    print("Average sentence length: "f"{stats.avgSentenceLength:.2f} words")
    print("Average syllable count in words: "f"{stats.avgWordSyllables:.2f}")
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