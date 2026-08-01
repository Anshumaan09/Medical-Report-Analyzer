import re
from models import (
    MedicalFinding,
    ReferenceRange,
    FindingStatus,
)


class CBCParser:
    """Parser for CBC reports."""

    HEMOGLOBIN_PATTERN = re.compile(
        r"Hemoglobin\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(g/dL|gm/dL)?",
        re.IGNORECASE
    )

    RANGE_PATTERN = re.compile(
        r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)"
    )

    @classmethod
    def parse(cls, text: str) -> list[MedicalFinding]:
        findings = []

        hemoglobin_match = cls.HEMOGLOBIN_PATTERN.search(text)

        if hemoglobin_match:
            value = float(hemoglobin_match.group(1))
            unit = hemoglobin_match.group(2) or "g/dL"

            # Try to find a reference range nearby
            range_match = cls.RANGE_PATTERN.search(text)

            reference_range = None
            status = FindingStatus.UNKNOWN

            if range_match:
                min_ref = float(range_match.group(1))
                max_ref = float(range_match.group(2))

                reference_range = ReferenceRange(
                    minimum=min_ref,
                    maximum=max_ref,
                    raw_text=f"{min_ref}-{max_ref}"
                )

                if value < min_ref:
                    status = FindingStatus.LOW
                elif value > max_ref:
                    status = FindingStatus.HIGH
                else:
                    status = FindingStatus.NORMAL

            findings.append(
                MedicalFinding(
                    test_name="Hemoglobin",
                    raw_value=str(value),
                    numeric_value=value,
                    unit=unit,
                    reference_range=reference_range,
                    status=status,
                    category="CBC"
                )
            )

        return findings