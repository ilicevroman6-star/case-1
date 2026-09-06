from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from application.use_cases import analyze_text, analyze_batch
from infrastructure.syllable_counters import get_syllable_counter
from infrastructure.sentiment import analyze_sentiment_textblob
from infrastructure.language_detector import detect_language
from infrastructure.cache import get_cached_result, set_cached_result
import redis

app = FastAPI()
templates = Jinja2Templates(directory="templates")

redis_client = redis.Redis.from_url("redis://localhost")

class TextRequest(BaseModel):
  text: str

class BatchRequest(BaseModel):
  texts: list[str]

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
def analyze_endpoint(request: TextRequest):
  text = request.text
  # проверка кэша
  cached = get_cached_result(redis_client, text)
  if cached:
    return cached
  # определение языка
  lang = detect_language(text)
  counter = get_syllable_counter(lang)
  try:
    result = analyze_text(text, detect_language, counter, analyze_sentiment_textblob)
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  set_cached_result(redis_client, text, result)
  return result.to_dict()

@app.post("/analyze-batch")
def analyze_batch_endpoint(request: BatchRequest):
  # можно также использовать кэш для каждого текста
  results = []
  for text in request.texts:
    cached = get_cached_result(redis_client, text)
    if cached:
      results.append(cached)
    else:
      lang = detect_language(text)
      counter = get_syllable_counter(lang)
      result = analyze_text(text, detect_language, counter, analyze_sentiment_textblob)
      set_cached_result(redis_client, text, result)
      results.append(result.to_dict())
  return results