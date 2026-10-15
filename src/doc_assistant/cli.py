import argparse
import sys
from pathlib import Path

from openai.types import CompletionUsage

from doc_assistant import assistant, config
from doc_assistant.pdf import NoTextError
from doc_assistant.prompts.loader import PromptNotFoundError


def format_usage(usage: CompletionUsage) -> str:
    cached = usage.prompt_tokens_details.cached_tokens if usage.prompt_tokens_details else 0
    reasoning = (
        usage.completion_tokens_details.reasoning_tokens if usage.completion_tokens_details else 0
    )
    line = (
        f"Tokens: {usage.prompt_tokens:,} in ({cached or 0:,} cached)"
        f" · {usage.completion_tokens:,} out ({reasoning or 0:,} reasoning)"
    )
    # OpenRouter adds "cost" (in USD credits), which is not a field of the OpenAI type.
    cost = (usage.model_extra or {}).get("cost")
    if cost is not None:
        line += f" · cost ${cost:.4f}"
    return line


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="main.py")
    commands = parser.add_subparsers(dest="command", required=True)
    ask = commands.add_parser("ask", help="Answer a question about a PDF, with citations.")
    ask.add_argument("pdf", type=Path)
    ask.add_argument("question")
    args = parser.parse_args(argv)
    if not args.pdf.is_file():
        parser.error(f"file not found: {args.pdf}")

    try:
        settings = config.load_settings()
        answer = assistant.ask(args.pdf, args.question, settings)
    except (config.ConfigError, PromptNotFoundError, NoTextError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if answer.pages_without_text:
        print(
            f"Warning: {len(answer.pages_without_text)} page(s) have no text and are not used: "
            + ", ".join(map(str, answer.pages_without_text)),
            file=sys.stderr,
        )
    print(answer.text)
    print()
    print(format_usage(answer.usage))
    return 0
