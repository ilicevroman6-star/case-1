from collections import Counter

from infrastructure.additional_metrics import rareWordDensity, lexicalDiversity, tokenize
from infrastructure.validation import validateText
from infrastructure.sentiment import translateToEnglish, analyzeSentimentTextblob
from domain.types import Polarity
from domain.types import Language

def testTranslateToEnglish():
  result = translateToEnglish("Bonjour")
  assert isinstance(result, str)
  assert len(result) > 0


def testPositiveSentiment():
  result = analyzeSentimentTextblob("J'adore ce film")
  assert result[0] == Polarity.POSITIVE


def testNegativeSentiment():
  result = analyzeSentimentTextblob("Je déteste ce film")
  assert result[0] == Polarity.NEGATIVE


def testNeutralSentiment():
  result = analyzeSentimentTextblob("La table est dans la pièce")
  assert result[0] == Polarity.NEUTRAL

def testTokenizeEnglish():
  text = "The cat and the dog."
  expected = ["the", "cat", "and", "the", "dog"]

  assert tokenize(text) == expected


def testTokenizeRussian():
  text = "Привет, мир! Это тест."
  expected = ["привет", "мир", "это", "тест"]

  assert tokenize(text) == expected


def testTokenizeFrench():
  text = "L'amour est important."
  expected = ["l'amour", "est", "important"]

  assert tokenize(text) == expected


def testTokenizeGerman():
  text = "Der Text für die Schule."
  expected = ["der", "text", "für", "die", "schule"]

  assert tokenize(text) == expected


def testTokenizeRemovesNumbers():
  text = "Text 123 456 test."
  expected = ["text", "test"]

  assert tokenize(text) == expected


def testLexicalDiversitySimple():
  text = "cat cat dog"

  assert lexicalDiversity(text) == 2 / 3


def testLexicalDiversityAllUnique():
  text = "cat dog mouse"

  assert lexicalDiversity(text) == 1.0


def testLexicalDiversityEmptyText():
  text = ""

  assert lexicalDiversity(text) == 0


def testRareWordDensityDict():
  freq_dict = {
    "the": 100,
    "cat": 5,
    "dog": 1,
    "mouse": 0,
  }

  text = "the cat dog mouse"
  assert rareWordDensity(text, freq_dict, threshold=2) == 0.5


def testRareWordDensityCounter():
  freq_counter = Counter({
    "the": 100,
    "cat": 5,
    "dog": 1,
  })

  text = "the cat dog unknown"
  assert rareWordDensity(text, freq_counter, threshold=2) == 0.5


def testRareWordDensityEmptyText():
  freq_dict = {
    "the": 100,
    "cat": 5,
  }

  assert rareWordDensity("", freq_dict, threshold=2) == 0




if __name__ == "__main__":
    testTranslateToEnglish()
    testPositiveSentiment()
    testNegativeSentiment()
    testNeutralSentiment()
    testTokenizeEnglish()
    testTokenizeRussian()
    testTokenizeFrench()
    testTokenizeGerman()
    testTokenizeRemovesNumbers()
    testLexicalDiversitySimple()
    testLexicalDiversityAllUnique()
    testLexicalDiversityEmptyText()
    testRareWordDensityDict()
    testRareWordDensityCounter()
    testRareWordDensityEmptyText()

    print("All tests passed")