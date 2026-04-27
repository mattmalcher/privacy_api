from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_path: str | None = None   # None → ~/.opf/privacy_filter (auto-download)
    device: str = "cuda"            # "cuda" or "cpu" — OPF does not accept int indices
    output_mode: str = "typed"      # "typed" or "redacted"
    decode_mode: str = "viterbi"    # "viterbi" (CRF) or "argmax" (faster)
    trim_whitespace: bool = True
    discard_overlapping_predicted_spans: bool = False

    model_config = {"env_prefix": "PRIVACY_"}


settings = Settings()
