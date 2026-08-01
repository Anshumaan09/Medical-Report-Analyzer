from pathlib import Path
import fitz

from ingestion.ocr import OCRProcessor


class PDFLoader:
    """Hybrid PDF loader with automatic OCR fallback."""

    MIN_TEXT_THRESHOLD = 100

    @staticmethod
    def extract_text_direct(pdf_path: str | Path) -> str:
        document = fitz.open(pdf_path)

        pages = []

        for page in document:
            text = page.get_text()
            if text.strip():
                pages.append(text)

        document.close()

        return "\n".join(pages)

    @classmethod
    def extract_text(cls, pdf_path: str | Path) -> str:
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        direct_text = cls.extract_text_direct(pdf_path)

        if len(direct_text.strip()) >= cls.MIN_TEXT_THRESHOLD:
            print(f"Using direct PDF text extraction")
            print(f"Extracted {len(direct_text)} characters")
            return direct_text

        print("Direct extraction insufficient - switching to OCR fallback")

        ocr_text = OCRProcessor.extract_text_from_pdf(pdf_path)

        print(f"OCR extracted {len(ocr_text)} characters")

        return ocr_text