from models import MedicalReport, FindingStatus


class SummaryService:
    """Generate report-level summaries."""

    @staticmethod
    def generate_summary(report: MedicalReport) -> dict:
        abnormal = []
        normal_count = 0

        for finding in report.findings:
            if finding.status in (FindingStatus.LOW, FindingStatus.HIGH):
                abnormal.append(
                    {
                        "test_name": finding.test_name,
                        "status": finding.status.value,
                        "value": f"{finding.raw_value} {finding.unit or ''}",
                    }
                )
            else:
                normal_count += 1

        # Create human-readable summary
        if abnormal:
            abnormal_tests = ", ".join(item["test_name"] for item in abnormal)

            overview = (
                f"This CBC report contains {len(abnormal)} abnormal finding(s): "
                f"{abnormal_tests}. Most other parameters appear to be within "
                f"their reference ranges."
            )
        else:
            overview = (
                "All extracted CBC parameters appear to be within their "
                "reference ranges."
            )

        return {
            "overview": overview,
            "abnormal_findings_count": len(abnormal),
            "normal_findings_count": normal_count,
            "abnormal_findings": abnormal,
        }