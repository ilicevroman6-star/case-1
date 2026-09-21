import redis
from application.use_cases import analyzeBatch, analyzeText
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from infrastructure.cache import get_cached_result, set_cached_result
from infrastructure.language_detector import detectLanguage
from infrastructure.sentiment import analyzeSentimentTextblob
from infrastructure.syllable_counters import getSyllableCounter
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

redis_client = redis.Redis.from_url('redis://localhost')

class TextRequest(BaseModel):
  text: str

class BatchRequest(BaseModel):
  texts: list[str]

@app.get('/', response_class=HTMLResponse)
def read_root(request: Request):
  return templates.TemplateResponse(
    request=request,
    name='index.html',
    context={}
  )

@app.post('/analyze')
def analyzeEndpoint(request: TextRequest):
  text = request.text
  # проверка кэша
  cached = get_cached_result(redis_client, text)
  if cached:
    return cached
  # определение языка
  lang = detectLanguage(text)
  counter = getSyllableCounter(lang)
  try:
    result = analyzeText(text, detectLanguage, counter, analyzeSentimentTextblob)
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  set_cached_result(redis_client, text, result)
  # Вместо return result.model_dump() напишите:
  return jsonable_encoder(result)


@app.post('/analyze-batch')
def analyzeBatchEndpoint(request: BatchRequest):
  # можно также использовать кэш для каждого текста
  results = []
  for text in request.texts:
    cached = get_cached_result(redis_client, text)
    if cached:
      results.append(cached)
    else:
      lang = detectLanguage(text)
      counter = getSyllableCounter(lang)
      result = analyzeText(text, detectLanguage, counter, analyzeSentimentTextblob)
      set_cached_result(redis_client, text, result)
      results.append(jsonable_encoder(result))
  return results
