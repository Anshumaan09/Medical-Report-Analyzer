from retrieval.retriever import MedicalRetriever


retriever = MedicalRetriever()

query = "What does low hemoglobin mean?"

docs = retriever.retrieve(query)

print(f"Query: {query}\n")

for i, doc in enumerate(docs, start=1):
    print(f"RESULT {i}")
    print("-" * 50)
    print(doc.page_content)
    print()