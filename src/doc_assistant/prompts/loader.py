from importlib.resources import files


class PromptNotFoundError(Exception):
    pass


def load_prompt(version: str) -> str:
    prompts = files("doc_assistant.prompts")
    available = sorted(p.name.removesuffix(".txt") for p in prompts.iterdir() if p.name.endswith(".txt"))
    if version not in available:
        raise PromptNotFoundError(
            f"Prompt version '{version}' does not exist. Available: {', '.join(available) or 'none'}"
        )
    return (prompts / f"{version}.txt").read_text(encoding="utf-8").strip()
