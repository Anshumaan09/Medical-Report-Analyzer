import requests
import streamlit as st

from services.rag_qa_service import MedicalRAGQAService


API_URL = "http://127.0.0.1:8000/analyze"


st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🩺",
    layout="wide",
)


st.title("🩺 AI Medical Report Analyzer with RAG")
st.markdown(
    "Upload a **CBC PDF report** to get AI-powered explanations, a structured summary, and test the **RAG knowledge retrieval system**."
)


# =====================================================
# PDF REPORT ANALYSIS
# =====================================================

uploaded_file = st.file_uploader(
    "Choose a PDF report",
    type=["pdf"],
)


if uploaded_file is not None:
    with st.spinner("Analyzing report..."):
        files = {
            "file": (uploaded_file.name, uploaded_file, "application/pdf")
        }

        response = requests.post(API_URL, files=files)

    if response.status_code == 200:
        data = response.json()

        st.success("Report analyzed successfully!")

        # -------------------- Summary --------------------
        summary = data.get("summary", {})

        st.header("📋 Report Summary")
        st.info(summary.get("overview", "No summary available."))

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Abnormal Findings",
                summary.get("abnormal_findings_count", 0),
            )

        with col2:
            st.metric(
                "Normal Findings",
                summary.get("normal_findings_count", 0),
            )

        # -------------------- Abnormal Findings --------------------
        abnormal = summary.get("abnormal_findings", [])

        if abnormal:
            st.header("⚠️ Abnormal Findings")

            for item in abnormal:
                st.error(
                    f"**{item['test_name']}** → "
                    f"{item['value']} ({item['status'].upper()})"
                )

        # -------------------- Detailed Findings --------------------
        st.header("🧪 Detailed Results")

        for finding in data.get("findings", []):
            with st.expander(
                f"{finding['test_name']} — {finding['status'].upper()}"
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(
                        f"**Value:** {finding['raw_value']} {finding.get('unit', '')}"
                    )
                    st.write(f"**Status:** {finding['status']}")

                    if finding.get("lab_flag"):
                        st.write(f"**Lab Flag:** {finding['lab_flag']}")

                with col2:
                    if finding.get("reference_range"):
                        st.write(
                            f"**Reference Range:** "
                            f"{finding['reference_range']['raw_text']}"
                        )

                st.markdown("**🧠 RAG-Grounded AI Explanation**")
                st.write(
                    finding.get("explanation", "No explanation available.")
                )

        # -------------------- Download JSON --------------------
        st.download_button(
            label="📥 Download JSON Report",
            data=response.text,
            file_name="medical_report_analysis.json",
            mime="application/json",
        )

    else:
        st.error(f"API Error: {response.status_code}")
        st.text(response.text)


# =====================================================
# RAG KNOWLEDGE PLAYGROUND
# =====================================================

st.divider()
st.header("🧠 Medical RAG Playground")

st.markdown(
    "Ask questions to verify that the **Retrieval-Augmented Generation (RAG)** system retrieves the correct medical knowledge from **ChromaDB** before generating the answer."
)

question = st.text_input(
    "Ask a medical knowledge question",
    placeholder="What does low hemoglobin mean?",
)


if st.button("Ask RAG") and question:
    with st.spinner("Retrieving medical knowledge and generating answer..."):
        try:
            rag_service = MedicalRAGQAService()
            result = rag_service.ask(question)

            # -------------------- Grounded Answer --------------------
            st.subheader("🤖 Grounded Answer")
            st.success(result["answer"])

            # -------------------- Retrieved Context --------------------
            st.subheader("📚 Retrieved Context from ChromaDB")

            for i, chunk in enumerate(result["retrieved_chunks"], start=1):
                with st.expander(f"Retrieved Chunk {i}"):
                    st.write(chunk)

        except Exception as e:
            st.error(f"RAG Error: {str(e)}")
