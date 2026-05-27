from pathlib import Path

import pandas as pd
from docx import Document as DocxDocument
from pypdf import PdfReader


def extract_text(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        doc = DocxDocument(str(path))
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    if suffix == ".csv":
        frame = pd.read_csv(path)
        return frame.to_csv(index=False)
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    raise ValueError("Unsupported file format")


def validate_extension(filename: str) -> None:
    allowed = {".pdf", ".docx", ".txt", ".csv"}
    if Path(filename).suffix.lower() not in allowed:
        raise ValueError("Supported formats are PDF, DOCX, TXT, and CSV")
