from retrieval.vector_store import MedicalVectorStore


if __name__ == "__main__":
    print("Building medical knowledge base...")

    db = MedicalVectorStore.build_knowledge_base()

    print(f"Stored chunks: {db._collection.count()}")