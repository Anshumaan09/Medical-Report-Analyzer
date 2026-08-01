import re

from models import (
    MedicalFinding,
    ReferenceRange,
    FindingStatus,
)


class CBCParser:
    """Generic configuration-driven CBC parser."""

    CBC_TESTS = {
        "hemoglobin": {
            "name": "Hemoglobin",
            "unit": "g/dL",
        },
        "hemoglobin (hb)": {
            "name": "Hemoglobin",
            "unit": "g/dL",
        },
        "mean corpuscular volume (mcv)": {
            "name": "MCV",
            "unit": "fL",
        },
        "mchc": {
            "name": "MCHC",
            "unit": "g/dL",
        },
        "mch": {
            "name": "MCH",
            "unit": "pg",
        },
        "total wbc count": {
            "name": "WBC Count",
            "unit": "cumm",
        },
        "platelet count": {
            "name": "Platelet Count",
            "unit": "cumm",
        },
        
        "packed cell volume (pcv)": {
            "name": "PCV",
            "unit": "%",
        },

        "total rbc count": {
            "name": "RBC Count",
            "unit": "mill/cumm",
        },

        "neutrophils": {
            "name": "Neutrophils",
            "unit": "%",
        },

        "lymphocytes": {
            "name": "Lymphocytes",
            "unit": "%",
        },

        "eosinophils": {
            "name": "Eosinophils",
            "unit": "%",
        },
    }

    VALUE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)")
    RANGE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)")

    LAB_FLAGS = {"low", "high", "borderline", "critical"}

    @classmethod
    def compute_status(
        cls, value: float, min_ref: float, max_ref: float
    ) -> FindingStatus:
        if value < min_ref:
            return FindingStatus.LOW
        elif value > max_ref:
            return FindingStatus.HIGH
        return FindingStatus.NORMAL

    @classmethod
    def parse(cls, text: str) -> list[MedicalFinding]:
        findings = []
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        for i, line in enumerate(lines):
            line_lower = line.lower()

            for keyword, config in cls.CBC_TESTS.items():
                if keyword in line_lower:
                    numbers = cls.VALUE_PATTERN.findall(line)

                    # Need at least one number for the test value
                    if not numbers:
                        continue

                    value = float(numbers[0])

                    # Try to find range on the same line
                    range_match = cls.RANGE_PATTERN.search(line)

                    # If not found, look in nearby lines
                    if not range_match:
                        nearby_text = "\n".join(lines[i:i+3])
                        range_match = cls.RANGE_PATTERN.search(nearby_text)

                    reference_range = None
                    status = FindingStatus.UNKNOWN

                    if range_match:
                        min_ref = float(range_match.group(1))
                        max_ref = float(range_match.group(2))

                        reference_range = ReferenceRange(
                            minimum=min_ref,
                            maximum=max_ref,
                            raw_text=f"{min_ref} - {max_ref}",
                        )

                        status = cls.compute_status(value, min_ref, max_ref)

                    # Detect lab flag (Low, High, Borderline, etc.)
                    lab_flag = None
                    for flag in cls.LAB_FLAGS:
                        if flag in line_lower:
                            lab_flag = flag.capitalize()
                            break

                    findings.append(
                        MedicalFinding(
                            test_name=config["name"],
                            raw_value=str(value),
                            numeric_value=value,
                            unit=config["unit"],
                            reference_range=reference_range,
                            status=status,
                            lab_flag=lab_flag,
                            category="CBC",
                        )
                    )

                    break

        return findings