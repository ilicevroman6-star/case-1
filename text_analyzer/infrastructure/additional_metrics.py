import re
from collections import Counter

TOKEN_RE = re.compile(r"[\w']+", flags = re.UNICODE)

def tokenize(text: str) -> list[str]:
  raw = TOKEN_RE.findall(text.lower())

  return [word for word in raw if any(ch.isalpha() for ch in word)]

def lexicalDiversity(text: str) -> float:
  words = tokenize(text)
  if not words:
    return 0
  return len(set(words)) / len(words)

def rareWordDensity(text: str, freqDict: dict | Counter, threshold: int = 2) -> float:
  words = tokenize(text)
  if not words:
    return 0

  rare = 0
  for word in words:
    count = freqDict.get(word, 0) if isinstance(freqDict, (dict, Counter)) else 0
    if count <= threshold:
      rare += 1

  return rare / len(words)