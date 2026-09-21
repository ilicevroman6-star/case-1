def validateText(text, max_length: int = 10000) -> bool:
  ALLOWED_PUNCT = set(".,;:!?()[]{}\"'«»„“”‘’–—-…\n\r\t ")

  if not isinstance(text, str):
    raise TypeError("text is not a string")

  if len(text.strip()) == 0:
    raise ValueError("text is empty")

  if len(text) > max_length:
    raise ValueError("text is too long")

  for ch in text:
    if ch.isalpha() or ch.isdigit() or ch.isspace() or ch in ALLOWED_PUNCT:
      continue
    raise ValueError("text contains invalid characters")

  return True