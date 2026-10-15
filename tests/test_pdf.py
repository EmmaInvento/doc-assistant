import pytest

from doc_assistant.pdf import NoTextError, Page, pages_without_text, read_pages


def test_read_pages_keeps_page_numbers(make_pdf):
    """Citations are only correct if each text keeps its real page number, also when a page
    in the middle has no text."""
    pages = read_pages(make_pdf(["First page", "", "Third page"]))

    assert pages == [
        Page(file="doc.pdf", number=1, text="First page"),
        Page(file="doc.pdf", number=2, text=""),
        Page(file="doc.pdf", number=3, text="Third page"),
    ]
    assert pages_without_text(pages) == [2]


def test_pdf_without_text_raises(make_pdf):
    """A scanned PDF has no text layer. The tool must say so, and not send an empty
    document to the model, which would only give a useless answer."""
    with pytest.raises(NoTextError, match="OCR"):
        read_pages(make_pdf(["", ""]))
