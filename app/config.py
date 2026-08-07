from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str
    
    # JWT Configuration
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
