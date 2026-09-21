import redis
from application.use_cases import analyzeBatch, analyzeText
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from infrastructure.cache import get_cached_result, set_cached_result
from infrastructure.language_detector import detectLanguage
from infrastructure.sentiment import analyzeSentimentTextblob
from infrastructure.syllable_counters import getSyllableCounter
from pydantic import BaseModel, field_validator
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

redis_client = redis.Redis.from_url('redis://localhost')
LANGUAGE_MAPPING = {
    1: "English",
    2: "Russian",
    3: "German",
    4: "French"
}


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
  result_dict = jsonable_encoder(result)
  if isinstance(result_dict, dict) and "language" in result_dict:
    lang_val = result_dict["language"]
    lookup_key = int(lang_val) if isinstance(lang_val, str) and lang_val.isdigit() else lang_val
    result_dict["language"] = LANGUAGE_MAPPING.get(lookup_key, lang_val)

  set_cached_result(redis_client, text, result_dict)
  return result_dict


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

      result_dict = jsonable_encoder(result)
      if isinstance(result_dict, dict) and "language" in result_dict:
        result_dict["language"] = LANGUAGE_MAPPING.get(result_dict["language"], result_dict["language"])

      set_cached_result(redis_client, text, result_dict)
      results.append(jsonable_encoder(result_dict))
  return results
