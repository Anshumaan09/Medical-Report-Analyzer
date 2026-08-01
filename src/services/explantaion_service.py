import os
from dotenv import load_dotenv
from groq import Groq

from models import MedicalFinding


load_dotenv()


class ExplanationService:
    """Generate simple-English explanations for medical findings."""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        self.client = Groq(api_key=api_key)

    def explain_finding(self, finding: MedicalFinding) -> str:
        prompt = f"""
            You are a medical report explanation assistant.

            Explain this blood test result in very simple English for a non-medical person.

            Test: {finding.test_name}
            Value: {finding.numeric_value} {finding.unit}
            Status: {finding.status.value}
            Reference Range: {finding.reference_range.raw_text if finding.reference_range else 'Unknown'}

            Rules:
            - Use 2-3 short sentences.
            - Do not give a diagnosis.
            - Do not prescribe medicines.
            - Mention that a healthcare professional should be consulted for proper interpretation.
            - Keep the tone reassuring and easy to understand.
                """

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You explain medical lab results in simple, safe, non-diagnostic language.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=120,
        )

        return response.choices[0].message.content.strip()