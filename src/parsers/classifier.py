from models import ReportType


class ReportClassifier:
    """Simple rule-based report classifier."""

    CBC_KEYWORDS = {
        "hemoglobin",
        "wbc",
        "rbc",
        "platelet",
        "mcv",
        "mch",
        "complete blood count",
    }

    LIPID_KEYWORDS = {
        "cholesterol",
        "hdl",
        "ldl",
        "triglycerides",
    }

    @classmethod
    def classify(cls, text: str) -> ReportType:
        text_lower = text.lower()

        if any(keyword in text_lower for keyword in cls.CBC_KEYWORDS):
            return ReportType.CBC

        if any(keyword in text_lower for keyword in cls.LIPID_KEYWORDS):
            return ReportType.LIPID_PROFILE

        return ReportType.UNKNOWN