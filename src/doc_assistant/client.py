from dataclasses import dataclass

from openai import OpenAI
from openai.types import CompletionUsage

from doc_assistant.config import Settings


@dataclass(frozen=True)
class Completion:
    text: str
    usage: CompletionUsage


def complete(messages: list[dict], settings: Settings) -> Completion:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=settings.api_key)
    response = client.chat.completions.create(model=settings.model, messages=messages)
    return Completion(text=response.choices[0].message.content, usage=response.usage)
