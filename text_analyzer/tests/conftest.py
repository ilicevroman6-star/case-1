import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """
    Фикстура для тестирования API.
    Создает тестового клиента FastAPI, который имитирует запросы
    к серверу без его реального запуска.
    """
    return TestClient(app)


@pytest.fixture
def sample_text():
    """
    Фикстура с примером текста на английском языке.
    """
    return "Hello world, how are you today?"


@pytest.fixture
def sample_text_russian():
    """
    Фикстура с примером текста на русском языке.
    """
    return "Привет мир, как у тебя дела?"