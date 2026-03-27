from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET: str
    JWT_EXPIRE_DAYS: int
    ENCRYPTION_KEY: str
    SENTRY_DSN: str
    APP_ENV: str
    PORT: int

    class Config:
        env_file = ".env"


settings = Settings()
