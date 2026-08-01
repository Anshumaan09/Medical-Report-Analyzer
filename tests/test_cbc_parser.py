from parsers.cbc_parser import CBCParser
from models import FindingStatus


def test_parse_hemoglobin():
    sample_report = """
    Complete Blood Count

    Hemoglobin: 10.2 g/dL
    Reference Range: 12.0 - 16.0
    """

    findings = CBCParser.parse(sample_report)

    assert len(findings) == 1

    finding = findings[0]

    assert finding.test_name == "Hemoglobin"
    assert finding.numeric_value == 10.2
    assert finding.status == FindingStatus.LOW
    assert finding.reference_range.minimum == 12.0
    assert finding.reference_range.maximum == 16.0