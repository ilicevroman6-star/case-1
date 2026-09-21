from collections import Counter
from application.use_cases import computeStats, analyzeText, fleschKincaid
from domain.interfaces import Language_Detector, Sentiment_Analyzer, Syllable_Counter
from infrastructure.flesch_calculators import fleschIndex, interpretFlesch
from infrastructure.language_detector import detectLanguage
from infrastructure.syllable_counters import getSyllableCounter
from infrastructure.sentiment import analyzeSentimentTextblob, translateToEnglish
from infrastructure.validation import validateText
from infrastructure.additional_metrics import lexicalDiversity, rareWordDensity
from fastapi import FastAPI
from logging_config import setup_logging
from structlog import get_logger
from prometheus_client import make_asgi_app
from metrics import REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT

setup_logging()
logger = get_logger()
app = FastAPI(
  title="Text Analysis Service",
  version="0.1.0",
  description="Synchronous text analysis service"
)

metrics_app = make_asgi_app()
app.mount('/metrics', metrics_app)

@app.get("/health")
async def health():
  REQUEST_COUNT.labels(method='GET', endpoint='/health', status='200').inc()
  logger.info("Health check", service="text-analyzer")
  return {"status": "ok", "service": "text-analyzer"}

def main() -> None:
  text = 'Я ненавижу этот мир'
  if validateText(text):
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
      print("Average sentence length: "f"{stats.avgSentenceLength:.2f}")
      print("Average syllable count in words: "f"{stats.avgWordSyllables:.2f}")
      print("Flesch index: "f"{flesch:.2f}")
      if flesch_kin is not None:
        print("Flesch-Kincaid index: "f"{flesch_kin:.2f}")
      else:
        print("Flesch-Kincaid index: unavailable")
      print("Interpret Flesch: "f"{interpret}")
      print("Polarity: "f"{polar.value}")
      print("Subjectivity: "f"{subj}")
      print("Lexical Diversity: "f"{lexicalDiversity(text)}")
      print("Rare word density: "f"{rareWordDensity(text, freqDict=Counter(text))}")

    except ValueError as error:
      print(f"Error: {error}")

if __name__ == "__main__":
    main()