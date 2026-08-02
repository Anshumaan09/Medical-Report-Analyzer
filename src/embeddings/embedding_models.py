from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingFactory:
    """Factory for creating embedding models."""

    @staticmethod
    def create():
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )