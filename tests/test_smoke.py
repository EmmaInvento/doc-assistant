from openai.types import CompletionUsage

from doc_assistant import client, config
from doc_assistant.cli import main


def test_question_about_pdf_gives_answer_and_token_line(make_pdf, monkeypatch, capsys):
    """The full path (CLI, settings, PDF, prompt file, prompt, client, output) works together.
    Only the network call is fake, so this test is free and does not need an API key."""
    sent = []

    def fake_complete(messages, settings):
        sent.append(messages)
        usage = CompletionUsage.model_validate(
            {
                "prompt_tokens": 98412,
                "completion_tokens": 1350,
                "total_tokens": 99762,
                "prompt_tokens_details": {"cached_tokens": 90000},
                "completion_tokens_details": {"reasoning_tokens": 1024},
                "cost": 0.0272,
            }
        )
        return client.Completion(text="Alpha is a letter [doc.pdf, p. 1]", usage=usage)

    monkeypatch.setattr(
        config, "load_settings", lambda: config.Settings("sk-test", "test-model", "v1")
    )
    monkeypatch.setattr(client, "complete", fake_complete)

    assert main(["ask", str(make_pdf(["Alpha", ""])), "What is alpha?"]) == 0

    out, err = capsys.readouterr()
    assert "Alpha is a letter [doc.pdf, p. 1]" in out
    assert (
        "Tokens: 98,412 in (90,000 cached) · 1,350 out (1,024 reasoning) · cost $0.0272" in out
    )
    assert "no text and are not used: 2" in err
    assert "cite its source" in sent[0][0]["content"]
    assert "[doc.pdf p. 1]\nAlpha" in sent[0][1]["content"]
