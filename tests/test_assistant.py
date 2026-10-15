from doc_assistant.assistant import build_messages
from doc_assistant.pdf import Page


def test_prompt_marks_pages_and_puts_question_last():
    """The model can only cite pages that are marked in the prompt. The question must come
    last so that the long document prefix is the same for each question and can be cached."""
    pages = [
        Page(file="notes.pdf", number=1, text="Alpha"),
        Page(file="notes.pdf", number=2, text=""),
        Page(file="notes.pdf", number=3, text="Gamma"),
    ]

    system, user = build_messages("SYSTEM", pages, "What is gamma?")

    assert system == {"role": "system", "content": "SYSTEM"}
    content = user["content"]
    assert "[notes.pdf p. 1]\nAlpha" in content
    assert "[notes.pdf p. 3]\nGamma" in content
    assert "p. 2]" not in content
    assert content.index("[notes.pdf p. 1]") < content.index("[notes.pdf p. 3]")
    assert content.endswith("Question: What is gamma?")
