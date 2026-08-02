from langchain_text_splitters import RecursiveCharacterTextSplitter


class MedicalTextSplitter:
    """Reusable text splitter for medical knowledge documents."""

    @staticmethod
    def get_splitter():
        return RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " "],
        )