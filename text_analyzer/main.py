from application.use_cases import computeStats, analyzeText, fleschKincaid
from domain.interfaces import Language_Detector, Sentiment_Analyzer, Syllable_Counter
from infrastructure.flesch_calculators import fleschIndex, interpretFlesch
from infrastructure.language_detector import detectLanguage
from infrastructure.syllable_counters import getSyllableCounter
from infrastructure.sentiment import analyzeSentimentTextblob, translateToEnglish

def main() -> None:
  text = "J’adore flâner dans les rues de Paris au printemps. Le soleil brille doucement et les arbres sont couverts de fleurs. Je m’arrête souvent pour admirer la façade des vieilles maisons. Parfois, je prends un café dans une petite brasserie accueillante. C’est à ce moment-là que je me sens vraiment heureux."

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
    translatedText = translateToEnglish(text)
    flesch_kin = fleschKincaid(translatedText)

    if language.value == 1:
      print("Language: English")
    if language.value == 2:
      print("Language: Russian")
    if language.value == 3:
      print("Language: German")
    if language.value == 4:
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