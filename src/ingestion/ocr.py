from pathlib import Path

import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


class OCRProcessor:
    """OCR processor for scanned PDF reports."""

    @staticmethod
    def preprocess_image(image_array: np.ndarray) -> np.ndarray:
        """Improve image quality for OCR."""

        # Convert to grayscale
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

        # Reduce noise
        denoised = cv2.GaussianBlur(gray, (3, 3), 0)

        # Binary thresholding
        processed = cv2.threshold(
            denoised,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )[1]

        return processed

    @classmethod
    def extract_text_from_pdf(cls, pdf_path: str | Path) -> str:
        """Extract text from scanned PDF using OCR."""

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        pages = convert_from_path(
            pdf_path,
            dpi=300,
            poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin",
        )

        extracted_pages = []

        for page in pages:
            image_array = np.array(page)
            processed_image = cls.preprocess_image(image_array)

            text = pytesseract.image_to_string(
                processed_image,
                config="--oem 3 --psm 6 -c preserve_interword_spaces=1",
            )

            if text.strip():
                extracted_pages.append(text)

        return "\n".join(extracted_pages)