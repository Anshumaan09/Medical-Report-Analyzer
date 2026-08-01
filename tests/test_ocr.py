from ingestion.pdf_loader import PDFLoader


text = PDFLoader.extract_text("data/raw/CBC_sample_report.pdf")

print("TEXT LENGTH:", len(text))
print(text[:500])