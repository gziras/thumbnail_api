from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    unsplash_access_key: str
    unsplash_api_url: str
    thumbnail_directory: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
