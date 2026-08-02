from langchain_community.vectorstores import Chroma

from embeddings.embedding_models import EmbeddingFactory
from retrieval.vector_store import MedicalVectorStore


class MedicalRetriever:
    """Semantic retriever for medical knowledge."""

    def __init__(self):
        embeddings = EmbeddingFactory.create()

        self.db = Chroma(
            persist_directory=MedicalVectorStore.PERSIST_DIRECTORY,
            embedding_function=embeddings,
        )

    def retrieve(self, query: str, k: int = 3):
        return self.db.similarity_search(query, k=k)