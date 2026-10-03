from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GROQ_API_KEY : str
    model:str="openai/gpt-oss-120b"
    DB_USER : str
    DB_PASSWORD : str




    model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding= "utf-8"
        )



setting = Settings()
    


