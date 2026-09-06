from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_seconds: int = 3600

    class Config:
        env_file = ".env"


settings = Settings()