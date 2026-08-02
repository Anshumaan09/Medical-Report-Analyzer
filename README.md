# 🩺 Medical Report Analyzer — AI + RAG

### Intelligent CBC Blood Report Analysis using **OCR, FastAPI, Streamlit, ChromaDB, and Groq Llama 3.3**

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-orange)
![Groq](https://img.shields.io/badge/Groq-Llama%203.3-purple)
![RAG](https://img.shields.io/badge/RAG-Enabled-success)

---

## 🚀 Overview

**Medical Report Analyzer** is a **full-stack AI application** that processes **CBC blood test PDF reports**, extracts medical findings using **OCR and structured parsing**, and generates **retrieval-grounded explanations** through a **Retrieval-Augmented Generation (RAG)** pipeline.

Unlike a simple LLM chatbot, this project combines:

* 📄 **Hybrid PDF extraction** (PyMuPDF + OCR fallback)
* 🧪 **Structured hematology parsing**
* 🧠 **Semantic medical knowledge retrieval**
* 📚 **ChromaDB vector database**
* 🤖 **Groq Llama 3.3 grounded explanations**
* 🌐 **FastAPI backend + Streamlit frontend**

---

## ✨ Key Features

### 📄 Document Intelligence

* Upload **CBC PDF reports**
* Automatic **text extraction** from digital PDFs
* **Tesseract OCR** support for scanned reports
* OpenCV-based image preprocessing for better OCR accuracy

### 🧪 Structured CBC Analysis

* Hemoglobin
* RBC Count
* WBC Count
* Platelet Count
* PCV / Hematocrit
* MCV / MCH / MCHC
* Differential WBC counts (Neutrophils, Lymphocytes, Eosinophils, etc.)

### 🧠 RAG Pipeline

* Medical knowledge documents stored locally
* Recursive semantic chunking
* Sentence-transformer embeddings (`all-MiniLM-L6-v2`)
* Persistent **ChromaDB** vector storage
* Semantic similarity retrieval
* Grounded explanation generation using **Groq Llama 3.3 70B**

### 🌐 User Experience

* Interactive **Streamlit dashboard**
* Highlighted **abnormal findings**
* Expandable detailed results
* **RAG Playground** for testing semantic retrieval
* Downloadable **JSON analysis report**

---

## 🏗️ Architecture

```text
                 ┌────────────────────┐
                 │   Streamlit UI     │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │    FastAPI API     │
                 └─────────┬──────────┘
                           │
        ┌──────────────────┴──────────────────┐
        ▼                                     ▼
 ┌───────────────┐                 ┌──────────────────┐
 │ PDF + OCR     │                 │  Medical Knowledge│
 └──────┬────────┘                 └─────────┬────────┘
        ▼                                    ▼
 ┌───────────────┐                 ┌──────────────────┐
 │ CBC Parser    │                 │ Semantic Chunking│
 └──────┬────────┘                 └─────────┬────────┘
        ▼                                    ▼
 ┌───────────────┐                 ┌──────────────────┐
 │ Structured    │                 │ SentenceTransformer│
 │ Findings      │                 │ Embeddings       │
 └──────┬────────┘                 └─────────┬────────┘
        ▼                                    ▼
 ┌────────────────────────────────────────────────┐
 │               ChromaDB Vector Store            │
 └───────────────────┬────────────────────────────┘
                         ▼
              ┌──────────────────────────────┐
              │ RAG Explanation Service     │
              │ 1. Retrieve relevant chunks │
              │ 2. Build grounded prompt    │
              │ 3. Generate Groq response   │
              └──────────────┬───────────────┘
                             ▼
              Patient-Friendly Explanation
```

---

## 📂 Project Structure

```text
Medical Report Analyzer/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── knowledge/
│   └── chroma_db/
│
├── src/
│   ├── api/
│   ├── chunking/
│   ├── embeddings/
│   ├── extraction/
│   ├── loaders/
│   ├── parsers/
│   ├── retrieval/
│   ├── services/
│   └── models.py
│
├── tests/
├── streamlit_app.py
├── build_knowledge_base.py
├── run_analysis.py
├── pyproject.toml
└── README.md
```

---

## ⚡ Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Anshumaan09/medical-report-analyzer.git
cd medical-report-analyzer
```

### 2️⃣ Install Dependencies

```bash
uv sync
```

### 3️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4️⃣ Build the Knowledge Base

```bash
python build_knowledge_base.py
```

### 5️⃣ Start the Backend

```bash
uvicorn src.api.main:app --reload
```

### 6️⃣ Start the Frontend

```bash
streamlit run streamlit_app.py
```

---

## 🧠 RAG Verification

Open the **Medical RAG Playground** in the Streamlit UI and ask:

```text
What does low hemoglobin mean?
```

The application will display:

* **Retrieved Context** from ChromaDB
* **Grounded Answer** generated by Groq using the retrieved knowledge

This confirms that the system is performing **Retrieval-Augmented Generation** rather than relying solely on the LLM’s internal memory.

---

## 🔍 Example Output

```json
{
  "test_name": "Hemoglobin",
  "numeric_value": 12.5,
  "unit": "g/dL",
  "status": "low",
  "explanation": "A low hemoglobin level may reduce the blood’s oxygen-carrying capacity. Retrieved medical knowledge suggests this can be associated with anemia or nutritional deficiencies, and a healthcare professional should interpret the result together with other findings."
}
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Test Semantic Retrieval

```bash
uv run python tests/test_retriever.py
```

### Test RAG Grounding

```bash
uv run python tests/test_rag_explanation.py
```

---

## 🛠️ Tech Stack

| Layer                | Technology            |
| -------------------- | --------------------- |
| **Backend**          | FastAPI               |
| **Frontend**         | Streamlit             |
| **OCR**              | Tesseract OCR         |
| **PDF Processing**   | PyMuPDF               |
| **Image Processing** | OpenCV                |
| **Embeddings**       | sentence-transformers |
| **Vector Database**  | ChromaDB              |
| **LLM**              | Groq Llama 3.3 70B    |
| **Language**         | Python 3.12           |

---

## 🎯 What This Project Demonstrates

This project showcases real-world **AI engineering skills**:

* OCR-based document ingestion
* Structured medical information extraction
* Semantic chunking strategies
* Embedding generation and vector storage
* Retrieval-Augmented Generation (RAG)
* Prompt grounding and hallucination reduction
* FastAPI microservice development
* Streamlit full-stack AI application development

---

## 🚧 Future Enhancements

* [ ] MRI / CT / X-Ray report support
* [ ] Medical entity extraction with MedSpaCy
* [ ] Source citation highlighting
* [ ] Retrieval score visualization
* [ ] Docker & cloud deployment
* [ ] User authentication and report history
* [ ] LangGraph multi-agent medical workflow

---

## ⚠️ Disclaimer

This project is intended for **educational and demonstration purposes only**. It does **not provide medical diagnoses, treatment recommendations, or professional healthcare advice**. Always consult a qualified healthcare professional for interpretation of laboratory results and medical decisions.

---

## 👨‍💻 Author

**Anshumaan Panigrahi**

* GitHub: **https://github.com/Anshumaan09**
* LinkedIn: **https://www.linkedin.com/in/anshumaanpanigrahi/**

---

## ⭐ Support

If you found this project useful or learned something about **RAG, OCR, FastAPI, or Streamlit**, please consider giving it a **⭐ star** on GitHub. It helps make the repository more visible to other developers and recruiters.

---

## 🟢 Project Status

### **Working End-to-End Medical RAG System**

* [x] PDF ingestion
* [x] OCR fallback
* [x] CBC parser
* [x] Structured findings extraction
* [x] FastAPI backend
* [x] Streamlit frontend
* [x] Semantic chunking
* [x] Embedding generation
* [x] ChromaDB persistence
* [x] Semantic retrieval
* [x] RAG-grounded Groq explanations
* [x] Web-based RAG playground

🚀 **This repository now implements a complete Retrieval-Augmented Generation pipeline integrated with a real medical document analysis application.**
