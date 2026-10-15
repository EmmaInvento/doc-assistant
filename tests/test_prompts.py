import pytest

from doc_assistant.prompts.loader import PromptNotFoundError, load_prompt


def test_unknown_prompt_version_fails_clearly():
    """A typo in PROMPT_VERSION must stop the tool with a message that lists the versions
    that exist, and not send the model an empty or wrong prompt."""
    with pytest.raises(PromptNotFoundError, match="'v99' does not exist. Available: v1"):
        load_prompt("v99")
