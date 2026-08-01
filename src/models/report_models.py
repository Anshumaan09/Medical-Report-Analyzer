from pydantic import BaseModel, Field
from models.finding_models import MedicalFinding, ReportType


class MedicalReport(BaseModel):
    report_type: ReportType = ReportType.UNKNOWN

    patient_name: str | None = None

    source_file: str | None = None

    raw_text: str = Field(..., description="Full extracted text from report")

    findings: list[MedicalFinding] = Field(default_factory=list)