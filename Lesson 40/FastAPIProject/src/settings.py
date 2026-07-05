from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str = "sqlite+aiosqlite:///sqlite3.db"
    SEED_SECRET: str = "x2r_xuYGg0OzHfhedMl6RoKu8D8ssqu_YWPxqiRMA3U"

settings = Settings()