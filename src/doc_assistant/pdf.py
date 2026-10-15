from dataclasses import dataclass
from pathlib import Path

import pymupdf


@dataclass(frozen=True)
class Page:
    file: str
    number: int  # 1-based, as printed in a PDF viewer
    text: str


class NoTextError(Exception):
    pass


def read_pages(path: Path) -> list[Page]:
    with pymupdf.open(path) as doc:
        pages = [
            Page(file=path.name, number=i + 1, text=page.get_text().strip())
            for i, page in enumerate(doc)
        ]
    if not any(page.text for page in pages):
        raise NoTextError(
            f"{path.name} has no text layer. It is probably scanned and needs OCR."
        )
    return pages


def pages_without_text(pages: list[Page]) -> list[int]:
    return [page.number for page in pages if not page.text]
