from pathlib import Path
import shutil
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from services.explantaion_service import ExplanationService
from services.analyse_servie import AnalysisService
from services.summary_service import SummaryService


app = FastAPI(
    title="Medical Report Analyzer",
    version="0.1.0",
    description="AI-powered medical report analysis API",
)

@app.get("/")
async def root():
    return {
        "message": "Medical Report Analyzer API",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze_report(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = Path(temp_file.name)

    try:
        report = AnalysisService.analyze_pdf(temp_path)

        # Generate explanations
        explanation_service = ExplanationService()

        findings_with_explanations = []

        for finding in report.findings:
            finding_data = finding.model_dump()

            finding_data["explanation"] = (
                explanation_service.explain_finding(finding)
            )

            findings_with_explanations.append(finding_data)

        summary = SummaryService.generate_summary(report)
        response = report.model_dump(exclude={"raw_text"})
        response["findings"] = findings_with_explanations
        response["summary"] = summary

        return response

    finally:
        temp_path.unlink(missing_ok=True)
