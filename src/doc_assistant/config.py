from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
REQUIRED_KEYS = ("OPENROUTER_API_KEY", "MODEL", "PROMPT_VERSION")


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Settings:
    api_key: str
    model: str
    prompt_version: str


def load_settings(env_file: Path = ENV_FILE) -> Settings:
    values = dotenv_values(env_file)
    missing = [key for key in REQUIRED_KEYS if not values.get(key)]
    if missing:
        raise ConfigError(f"Missing in {env_file}: {', '.join(missing)}")
    return Settings(
        api_key=values["OPENROUTER_API_KEY"],
        model=values["MODEL"],
        prompt_version=values["PROMPT_VERSION"],
    )
