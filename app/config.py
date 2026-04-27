from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_name: str = "openai/privacy-filter"
    device: int = 0
    max_batch_size: int = 32
    aggregation_strategy: str = "simple"

    model_config = {"env_prefix": "PRIVACY_"}


settings = Settings()
