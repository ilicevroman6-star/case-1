import hashlib
import json
import redis
from domain.types import AnalysisResult

def text_hash(text: str) -> str:
  return hashlib.sha256(text.encode()).hexdigest()

def get_cached_result(redis_client: redis.Redis, text: str):
  key = text_hash(text)
  data = redis_client.get(key)
  if data:
    return json.loads(data)
  return None

def set_cached_result(redis_client: redis.Redis, text: str, result: AnalysisResult):
  key = text_hash(text)
  redis_client.setex(key, 3600, json.dumps(result.to_dict()))  # TTL 1 час