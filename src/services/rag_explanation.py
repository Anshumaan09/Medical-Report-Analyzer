import os

from dotenv import load_dotenv
from groq import Groq

from models import MedicalFinding
from retrieval.retriever import MedicalRetriever


load_dotenv()


class RAGExplanationService:
    """Generate grounded explanations using retrieved medical knowledge."""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        self.client = Groq(api_key=api_key)
        self.retriever = MedicalRetriever()

    def explain_finding(self, finding: MedicalFinding) -> str:
        # Create retrieval query
        query = f"What does {finding.status.value} {finding.test_name} mean?"

        # Retrieve relevant medical knowledge
        docs = self.retriever.retrieve(query, k=3)

        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = f"""
You are a medical report explanation assistant.

Use ONLY the retrieved medical reference information below when generating the explanation.

Retrieved Medical Reference:
{context}

Lab Result:
- Test: {finding.test_name}
- Value: {finding.numeric_value} {finding.unit}
- Status: {finding.status.value}
- Reference Range: {finding.reference_range.raw_text if finding.reference_range else 'Unknown'}

Rules:
- Explain in simple English.
- Use 2-3 short sentences.
- Do not give a diagnosis.
- Do not prescribe medicines.
- Mention that a healthcare professional should interpret the result.
- Base the explanation on the retrieved reference information.
        """

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You explain medical lab results using retrieved reference information and avoid unsupported claims.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=120,
        )

        return response.choices[0].message.content.strip()