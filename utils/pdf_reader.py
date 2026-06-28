import os
import pdfplumber


def extract_text_from_pdf(file_path):
    text_chunks = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text() or ""
            text_chunks.append(extracted)
    return "\n".join(text_chunks)


def extract_text_from_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
        return handle.read()
