from embeddings.embedding_models import EmbeddingFactory


embeddings = EmbeddingFactory.create()

text = "Low hemoglobin may indicate anemia."

vector = embeddings.embed_query(text)

print(f"Text: {text}")
print(f"Vector length: {len(vector)}")
print(f"First 10 values: {vector[:10]}")