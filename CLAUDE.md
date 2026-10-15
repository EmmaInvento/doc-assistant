# Doc Assistant

A personal tool that answers questions about my documents (PDFs, notes, course slides),
citing which document and page each answer comes from.

## About me
I'm learning to use a coding assistant. Explain your choices briefly and keep changes small.

## Tech
- Python 3.12, virtual environment in .venv
- Development in VS Code on WSL
- LLM access through OpenRouter (API key in a .env file, never committed)

## Workflow
- Propose a plan before writing code for anything non-trivial.
- Write tests for new logic and run them.
- Keep the project runnable after every change.

## Engineering principles
- Do not preserve backward compatibility. Remove obsolete paths instead of adding compatibility layers, fallbacks, or migrations.
- Choose the simplest implementation that fully meets the current requirements. Avoid speculative abstractions, configuration, and indirection.
- Grow the system in layers. Start from the smallest version that works end to end, and add each new capability on top of a product that already works. Never trade a working product for unfinished complexity.
- Keep components modular and concerns clearly separated.
- Prefer established, well-maintained libraries when they reduce overall complexity or improve reliability. Do not reimplement common functionality without a clear reason.
- Lean on the dependencies already in the project before writing your own implementation or adding packages. Do not assume a library lacks a capability without checking its documentation and types.
- Make architectural decisions for the long term. Do not accept a stopgap that only works for now and is meant to be replaced later.
- Adhere as much as possible to the Simplified Technical English Standard ASD-STE100 when writing English.

## Architecture rules
- Settings come from .env and are loaded only in config.py. Other modules get settings from config.py.
- Only client.py calls the LLM API.
- Application logic has no terminal input or output; the CLI is a separate layer.
- Prompts are .txt files, one per version. Never edit an old version; add a new one.
- Documents live in data/, which is not committed. Never modify or delete files there.
- Prompts are loaded only through prompts/loader.py.