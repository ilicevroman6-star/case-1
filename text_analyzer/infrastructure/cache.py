import hashlib
import json
import redis
from domain.types import Analysis_Result
from fastapi.encoders import jsonable_encoder


def text_hash(text: str) -> str:
  return hashlib.sha256(text.encode()).hexdigest()

def get_cached_result(redis_client: redis.Redis, text: str):
  key = text_hash(text)
  data = redis_client.get(key)
  if data:
    return json.loads(data)
  return None

def set_cached_result(redis_client: redis.Redis, text: str, result: Analysis_Result):
  key = text_hash(text)
  # jsonable_encoder сам развернет все Enum (включая Language) в обычные строки
  redis_client.setex(key, 3600, json.dumps(jsonable_encoder(result)))  # TTL 1 час

