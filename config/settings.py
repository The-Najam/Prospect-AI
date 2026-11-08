from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GROQ_API_KEY : str
    GROQ_API_KEY_V2 : str
    GEMINI_API_KEY : str
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"
    GEMINI_MODEL_2: str = "gemini-3.1-flash-lite"
    model:str="openai/gpt-oss-120b"
    DB_USER : str
    DB_PASSWORD : str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    LANGSMITH_TRACING : bool
    LANGSMITH_API_KEY : str
    LANGSMITH_PROJECT : str
    CORS_ORIGINS : list[str]


    model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding= "utf-8"
        )


setting = Settings()




