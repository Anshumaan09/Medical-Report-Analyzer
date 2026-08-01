from enum import Enum
from pydantic import BaseModel, Field


class FindingStatus(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    UNKNOWN = "unknown"


class ReportType(str, Enum):
    CBC = "cbc"
    LIPID_PROFILE = "lipid_profile"
    LFT = "lft"
    KFT = "kft"
    UNKNOWN = "unknown"


class ReferenceRange(BaseModel):
    minimum: float | None = None
    maximum: float | None = None
    raw_text: str | None = None


class MedicalFinding(BaseModel):
    test_name: str = Field(..., description="Name of the medical test")

    raw_value: str = Field(..., description="Original extracted value from report")

    numeric_value: float | None = Field(
        default=None,
        description="Numeric value if available"
    )

    unit: str | None = Field(default=None, description="Measurement unit")

    reference_range: ReferenceRange | None = None

    status: FindingStatus = FindingStatus.UNKNOWN

    # Lab-provided flag (Low, High, Borderline, etc.)
    lab_flag: str | None = None

    category: str | None = None