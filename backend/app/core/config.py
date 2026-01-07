from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Personal Finance Manager"
    DATABASE_URL: str = "sqlite:///./finance.db"

    class Config:
        case_sensitive = True

settings = Settings()
