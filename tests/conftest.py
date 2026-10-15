from pathlib import Path

import pymupdf
import pytest


@pytest.fixture
def make_pdf(tmp_path):
    """Make a PDF with one page per item; an empty string gives a page with no text."""

    def make(page_texts: list[str], name: str = "doc.pdf") -> Path:
        path = tmp_path / name
        with pymupdf.open() as doc:
            for text in page_texts:
                page = doc.new_page()
                if text:
                    page.insert_text((72, 72), text)
            doc.save(path)
        return path

    return make
