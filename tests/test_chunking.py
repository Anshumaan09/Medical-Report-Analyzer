from chunking.text_splitter import MedicalTextSplitter


text = """
Low hemoglobin levels may suggest anemia, blood loss, or nutritional deficiencies.

Symptoms can include fatigue, weakness, dizziness, and shortness of breath.

A healthcare professional should interpret these results together with other blood parameters and clinical symptoms.
"""


splitter = MedicalTextSplitter.get_splitter()

chunks = splitter.split_text(text)

print(f"Total chunks: {len(chunks)}\n")

for i, chunk in enumerate(chunks, start=1):
    print(f"CHUNK {i}")
    print("-" * 40)
    print(chunk)
    print()