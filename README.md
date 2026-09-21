# case-1 — Text Analysis Service

Сервис для анализа текста: индекс Флеша, тональность и статистика.

## Технологии

- Python 3.11+
- FastAPI
- Redis (кэш)
- Docker
- Pytest (тесты)
- structlog (логирование)
- Prometheus (метрики)

## Запуск локально

1. Установите зависимости:
pip install -r requirements.txt

2. Запустите сервер:
cd text_analyzer
py -m uvicorn main:app --reload

3. Откройте в браузере:
- http://localhost:8000/health — проверка работы
- http://localhost:8000/docs — Swagger-документация
- http://localhost:8000/metrics — метрики Prometheus

## Запуск через Docker

docker-compose up --build

## Запуск тестов

py -m pytest text_analyzer/tests/ -v