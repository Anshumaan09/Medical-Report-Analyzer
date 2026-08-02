from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma

from chunking.text_splitter import MedicalTextSplitter
from embeddings.embedding_models import EmbeddingFactory


class MedicalVectorStore:
    """Build and manage the ChromaDB knowledge base."""

    PERSIST_DIRECTORY = "data/chroma_db"

    @classmethod
    def build_knowledge_base(cls):
        knowledge_dir = Path("data/knowledge")

        documents = []

        for file_path in knowledge_dir.glob("*.txt"):
            loader = TextLoader(str(file_path), encoding="utf-8")
            documents.extend(loader.load())

        print(f"Loaded {len(documents)} knowledge documents")

        # Chunk the documents
        splitter = MedicalTextSplitter.get_splitter()
        chunks = splitter.split_documents(documents)

        print(f"Created {len(chunks)} chunks")

        # Create embeddings
        embeddings = EmbeddingFactory.create()

        # Create Chroma vector database
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=cls.PERSIST_DIRECTORY,
        )

        print("ChromaDB knowledge base created successfully!")

        return vector_db