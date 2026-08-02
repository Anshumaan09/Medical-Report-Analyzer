from models import (
    MedicalFinding,
    ReferenceRange,
    FindingStatus,
)
from services.rag_explanation import RAGExplanationService


finding = MedicalFinding(
    test_name="Hemoglobin",
    raw_value="12.5",
    numeric_value=12.5,
    unit="g/dL",
    reference_range=ReferenceRange(
        minimum=13.0,
        maximum=17.0,
        raw_text="13.0 - 17.0",
    ),
    status=FindingStatus.LOW,
)


service = RAGExplanationService()

explanation = service.explain_finding(finding)

print("RAG-GROUNDED EXPLANATION")
print("=" * 50)
print(explanation)