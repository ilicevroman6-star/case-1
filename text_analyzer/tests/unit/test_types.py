from domain.types import Language, Polarity, Text_Stats


def test_language_enum():
    assert Language.EN.value == 1
    assert Language.RU.value == 2
    assert Language.DE.value == 3
    assert Language.FR.value == 4

def test_polarity_enum():
    assert Polarity.POSITIVE.value == "positive"

def test_text_stats_creation():
    stats = Text_Stats(
        sentenceCount=2,
        wordCount=10,
        syllableCount=15,
        avgSentenceLength=5.0,
        avgWordSyllables=1.5
    )
    assert stats.sentenceCount == 2
    assert stats.wordCount == 10
    assert stats.syllableCount == 15
