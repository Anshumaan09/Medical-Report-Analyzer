from services.analyse_servie import AnalysisService


if __name__ == "__main__":
    pdf_path = "data/raw/CBC_sample_report.pdf"

    report = AnalysisService.analyze_pdf(pdf_path)

    print("=" * 50)
    print(f"REPORT TYPE: {report.report_type.value}")
    print(f"SOURCE FILE: {report.source_file}")
    print("=" * 50)

    for finding in report.findings:
        print(f"Test: {finding.test_name}")
        print(f"Value: {finding.raw_value} {finding.unit or ''}")
        print(f"Computed Status: {finding.status.value}")

        if finding.lab_flag:
            print(f"Lab Flag: {finding.lab_flag}")

        if finding.reference_range:
            print(f"Reference: {finding.reference_range.raw_text}")

        print("-" * 50)