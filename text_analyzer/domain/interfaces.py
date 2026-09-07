from typing import Protocol

from domain.types import Language, Polarity


class Syllable_Counter(Protocol):
  def __call__(self, word: str) -> int:
    ...

class Sentiment_Analyzer(Protocol):
  def __call__(self, text: str) -> tuple[Polarity, float]:
    ...

class Language_Detector(Protocol):
  def __call__(self, text: str) -> Language:
    ...