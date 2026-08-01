from models import (
    MedicalFinding,
    ReferenceRange,
    FindingStatus,
)


def test_medical_finding_creation():
    finding = MedicalFinding(
        test_name="Hemoglobin",
        raw_value="10.2",
        numeric_value=10.2,
        unit="g/dL",
        reference_range=ReferenceRange(
            minimum=12.0,
            maximum=16.0,
            raw_text="12.0 - 16.0"
        ),
        status=FindingStatus.LOW,
        category="CBC"
    )

    assert finding.numeric_value == 10.2
    assert finding.status == FindingStatus.LOW
    assert finding.reference_range.minimum == 12.0