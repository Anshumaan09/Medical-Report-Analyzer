from pathlib import Path

from ingestion.pdf_loader import PDFLoader
from models import MedicalReport, ReportType
from parsers.classifier import ReportClassifier
from parsers.cbc_parser import CBCParser


class AnalysisService:
    """Main service for analyzing medical reports."""

    @staticmethod
    def analyze_pdf(pdf_path: str | Path) -> MedicalReport:
        raw_text = PDFLoader.extract_text(pdf_path)

        report_type = ReportClassifier.classify(raw_text)

        findings = []

        if report_type == ReportType.CBC:
            findings = CBCParser.parse(raw_text)

        return MedicalReport(
            report_type=report_type,
            source_file=str(pdf_path),
            raw_text=raw_text,
            findings=findings,
        )