from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GROQ_API_KEY : str
    GROQ_API_KEY_V2 : str
    GEMINI_API_KEY : str
    GEMINI_MODEL : str = "models/gemini-3.6-flash"
    GEMINI_MODEL_2 : str = "models/gemini-3.1-flash-lite"
    model:str="openai/gpt-oss-120b"
    DB_USER : str
    DB_PASSWORD : str


    model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding= "utf-8"
        )


setting = Settings()




