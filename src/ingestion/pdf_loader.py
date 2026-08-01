from pathlib import Path
import fitz  # PyMuPDF


class PDFLoader:
    """Load and extract text from PDF files."""

    @staticmethod
    def extract_text(pdf_path: str | Path) -> str:
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        document = fitz.open(pdf_path)

        pages = []

        for page in document:
            text = page.get_text()
            if text.strip():
                pages.append(text)

        document.close()

        return "\n".join(pages)