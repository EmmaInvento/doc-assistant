# Roadmap

Each step adds a capability on top of a working product. See [CLAUDE.md](../CLAUDE.md) for the
engineering rules and the project structure.

## Libraries

| Purpose | Library | Why |
|---------|---------|-----|
| PDF text | PyMuPDF | Fast, good text extraction from slides and columns, simple per-page API. |
| LLM calls | `openai` SDK with OpenRouter | OpenRouter has an OpenAI-compatible API; the SDK gives retries, timeouts and typed responses. |
| Vector store | Chroma | Local, persistent, no server, keeps file and page metadata with each chunk. |
| Tests | pytest | Standard for Python. |
| Environment | uv | Installs Python 3.12, manages `.venv`, dependencies and the lock file. |

## Step 1: Minimum version — in progress

One PDF, one question, an answer with page citations.

- [x] Read the PDF page by page; stop with a clear error if it has no text layer; warn about pages with no text.
- [x] Send the full document (with page markers) and the question to `openai/gpt-5-mini`.
- [x] Print the answer with `[file, p. N]` citations and the token use (input, cached, output, reasoning, cost).
- [x] Settings from `.env`; prompt versions as files in `prompts/`.
- [x] Project structure and tests as in CLAUDE.md.
- [ ] Commit.


Known: pages 27, 95 and 107 of the current PDF have no text (probably images only).

## Step 2: Measure quality

- Tracing with Phoenix: record each request (prompt, answer, tokens, time).
- Golden set: questions with the expected file and page.
- Experiments: run the golden set with different prompt versions and compare the results.

## Step 3: More documents and chat

- Multiple documents: split pages into chunks, make embeddings, store them in Chroma, and send only
  the relevant chunks to the model. Each chunk keeps its file and page.
- Chat history: follow-up questions that depend on earlier questions and answers.

To decide in this step: the embedding model (first choice: an embedding model through OpenRouter,
if available; else a local model with fastembed).

## Step 4: Trustworthy citations and a GUI

- Structured output: the answer plus a list of citations `{file, page, quote}`. The code checks
  that each quote is on the cited page and marks the citations that fail.
- A simple GUI that shows the answer, its citations and the source passages.

To decide in this step: the GUI library.

## Later, only if needed

- Incremental indexing (process only new or changed files).
- More file formats (Markdown notes, PPTX slides).
- Hybrid search (keywords + vectors) or reranking.


## Next session

- [ ] Understand if it is better to switch to client.responses.create() as usually
- [ ] Understand why is doing reasoning, eliminate it if it is too much
- [ ] Understand if should be told explicitely when a prompt pattern should be applied
