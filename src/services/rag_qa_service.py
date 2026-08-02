from groq import Groq
from dotenv import load_dotenv
import os

from retrieval.retriever import MedicalRetriever

load_dotenv()


class MedicalRAGQAService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.retriever = MedicalRetriever()

    def ask(self, question: str):
        docs = self.retriever.retrieve(question, k=3)

        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = f"""
Answer the question using ONLY the retrieved medical reference information.

Retrieved Information:
{context}

Question: {question}

Provide a simple, safe explanation for a non-medical user.
        """

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions using retrieved medical knowledge only.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=150,
        )

        return {
            "answer": response.choices[0].message.content.strip(),
            "retrieved_chunks": [doc.page_content for doc in docs],
        }