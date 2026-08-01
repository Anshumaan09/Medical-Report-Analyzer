import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/analyze"


st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🩺",
    layout="wide",
)


st.title("🩺 AI Medical Report Analyzer")
st.markdown("Upload a **CBC PDF report** to get AI-powered explanations and a structured summary.")


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

        # Summary section
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

        # Abnormal findings highlight
        abnormal = summary.get("abnormal_findings", [])

        if abnormal:
            st.header("⚠️ Abnormal Findings")

            for item in abnormal:
                st.error(
                    f"**{item['test_name']}** → "
                    f"{item['value']} ({item['status'].upper()})"
                )

        # Detailed findings
        st.header("🧪 Detailed Results")

        for finding in data.get("findings", []):
            with st.expander(f"{finding['test_name']} — {finding['status'].upper()}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Value:** {finding['raw_value']} {finding.get('unit', '')}")
                    st.write(f"**Status:** {finding['status']}")

                    if finding.get("lab_flag"):
                        st.write(f"**Lab Flag:** {finding['lab_flag']}")

                with col2:
                    if finding.get("reference_range"):
                        st.write(
                            f"**Reference Range:** "
                            f"{finding['reference_range']['raw_text']}"
                        )

                st.markdown("**AI Explanation**")
                st.write(finding.get("explanation", "No explanation available."))

        # Download JSON
        st.download_button(
            label="📥 Download JSON Report",
            data=response.text,
            file_name="medical_report_analysis.json",
            mime="application/json",
        )

    else:
        st.error(f"API Error: {response.status_code}")
        st.text(response.text)