from dataclasses import dataclass
from pathlib import Path

from openai.types import CompletionUsage

from doc_assistant import client
from doc_assistant.config import Settings
from doc_assistant.pdf import Page, pages_without_text, read_pages
from doc_assistant.prompts.loader import load_prompt


@dataclass(frozen=True)
class Answer:
    text: str
    usage: CompletionUsage
    pages_without_text: list[int]


def build_messages(system_prompt: str, pages: list[Page], question: str) -> list[dict]:
    # The document comes before the question, so that the long prefix is the same
    # for each question and the provider can cache it.
    document = "\n\n".join(
        f"[{page.file} p. {page.number}]\n{page.text}" for page in pages if page.text
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"<document>\n{document}\n</document>\n\nQuestion: {question}"},
    ]


def ask(pdf_path: Path, question: str, settings: Settings) -> Answer:
    pages = read_pages(pdf_path)
    messages = build_messages(load_prompt(settings.prompt_version), pages, question)
    completion = client.complete(messages, settings)
    return Answer(
        text=completion.text,
        usage=completion.usage,
        pages_without_text=pages_without_text(pages),
    )
