from domain.types import Language, Polarity, TextStats

def test_language_enum():
    assert Language.EN.value == 1
    assert Language.RU.value == 2
    assert Language.DE.value == 3
    assert Language.FR.value == 4

def test_polarity_enum():
    assert Polarity.POSITIVE.value == "positive"

def test_text_stats_creation():
    stats = TextStats(
        sentence_count=2,
        word_count=10,
        syllable_count=15,
        avg_sentence_length=5.0,
        avg_word_syllables=1.5
    )
    assert stats.sentence_count == 2