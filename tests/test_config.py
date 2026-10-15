import pytest

from doc_assistant.config import ConfigError, Settings, load_settings


def test_settings_load_from_env_file(tmp_path):
    """All settings come from the .env file, so a wrong key name or mapping shows up here
    and not as a confusing API error later."""
    env_file = tmp_path / ".env"
    env_file.write_text("OPENROUTER_API_KEY=sk-test\nMODEL=openai/gpt-5-mini\nPROMPT_VERSION=v1\n")

    assert load_settings(env_file) == Settings(
        api_key="sk-test", model="openai/gpt-5-mini", prompt_version="v1"
    )


def test_missing_api_key_fails_clearly(tmp_path):
    """Without an API key the tool must stop before any request and name the missing key."""
    env_file = tmp_path / ".env"
    env_file.write_text("MODEL=openai/gpt-5-mini\nPROMPT_VERSION=v1\n")

    with pytest.raises(ConfigError, match="OPENROUTER_API_KEY"):
        load_settings(env_file)
