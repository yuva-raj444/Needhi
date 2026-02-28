# 🇮🇳 NyayaSahaya — AI-Powered Multilingual Legal Assistant for India

> An intelligent legal assistant that answers questions in **Tamil + English**, drafts formal complaints, and classifies legal issues — powered by RAG over Indian law.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![React](https://img.shields.io/badge/React-18-cyan) ![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **RAG Q&A** | Ask legal questions → retrieves relevant Indian law sections → generates simplified answers |
| 🏷️ **Issue Classifier** | Auto-classifies issues into Criminal / Civil / Family / Consumer / Land / Welfare |
| 📝 **Complaint Drafter** | Generates formal legal complaints as downloadable PDFs |
| 🌐 **Multilingual** | Auto-detects Tamil / English and responds in the same language |
| ⚖️ **Indian Law Focus** | IPC, CrPC, Consumer Protection Act, Domestic Violence Act, and more |
| 🛡️ **Safety Disclaimer** | Built-in legal disclaimer on every response |

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────────────────────┐
│   React Frontend│◄────────►│       FastAPI Backend             │
│   (Port 3000)   │  REST   │       (Port 8000)                │
└─────────────────┘         │                                  │
                            │  ┌────────────┐ ┌─────────────┐ │
                            │  │ RAG Engine │ │  Classifier  │ │
                            │  │  (FAISS +  │ │  (LLM-based) │ │
                            │  │  OpenAI)   │ │              │ │
                            │  └────────────┘ └─────────────┘ │
                            │  ┌────────────┐ ┌─────────────┐ │
                            │  │ Complaint  │ │  Language    │ │
                            │  │ Generator  │ │  Detector    │ │
                            │  │ + PDF      │ │  + Translate │ │
                            │  └────────────┘ └─────────────┘ │
                            │  ┌─────────────────────────────┐ │
                            │  │     FAISS Vector Store       │ │
                            │  └─────────────────────────────┘ │
                            └──────────────────────────────────┘
```

---

## 📁 Project Structure

```
niral/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry
│   │   ├── config.py            # Settings & environment config
│   │   ├── routers/             # API endpoints
│   │   │   ├── query.py         # RAG Q&A endpoint
│   │   │   ├── classifier.py    # Legal issue classifier
│   │   │   ├── complaint.py     # Complaint draft + PDF
│   │   │   └── documents.py     # Document upload & indexing
│   │   ├── services/            # Business logic
│   │   │   ├── rag_service.py   # RAG pipeline
│   │   │   ├── llm_service.py   # OpenAI wrapper
│   │   │   ├── embedding_service.py  # Embedding + FAISS
│   │   │   ├── classifier_service.py # Classification logic
│   │   │   ├── complaint_service.py  # Complaint generation
│   │   │   ├── language_service.py   # Language detect + translate
│   │   │   └── pdf_service.py   # PDF generation
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── utils/
│   │   │   ├── text_processor.py # Text chunking utilities
│   │   │   └── constants.py     # App-wide constants
│   │   └── data/
│   │       ├── vector_store/    # FAISS index storage
│   │       └── sample_docs/     # Example legal documents
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── public/index.html
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── ComplaintForm.jsx
│   │   │   ├── ClassifierPanel.jsx
│   │   │   ├── DocumentUpload.jsx
│   │   │   ├── Disclaimer.jsx
│   │   │   └── LanguageToggle.jsx
│   │   ├── services/api.js
│   │   └── utils/constants.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key

### 1. Clone & Setup Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

# Create .env from template
copy .env.example .env       # Windows
# cp .env.example .env       # Mac/Linux

# Edit .env and add your OpenAI API key
```

### 2. Index Sample Legal Documents

```bash
# Start backend first, then use the /documents/index endpoint
# or place .txt files in backend/app/data/sample_docs/
```

### 3. Start Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Start Frontend

```bash
cd frontend
npm install
npm start
```

Open **http://localhost:3000** in your browser.

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## ☁️ Cloud Deployment

### Backend → Render.com
1. Create a new **Web Service** on Render
2. Connect your GitHub repo
3. Set root directory: `backend`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add env var: `OPENAI_API_KEY=your_key`

### Frontend → Netlify
1. Create a new site on Netlify
2. Build command: `npm run build`
3. Publish directory: `frontend/build`
4. Add env var: `REACT_APP_API_URL=https://your-render-backend.onrender.com`

---

## 📊 Example Legal Dataset Format

Place `.txt` files in `backend/app/data/sample_docs/`. Each file should contain sections of Indian law:

```
SECTION 302 — PUNISHMENT FOR MURDER
Whoever commits murder shall be punished with death, or imprisonment for life,
and shall also be liable to fine.

SECTION 304 — PUNISHMENT FOR CULPABLE HOMICIDE NOT AMOUNTING TO MURDER
...
```

Supported formats: `.txt`, `.pdf` (auto-parsed)

---

## 💬 Example Prompts

| Query | Expected Behavior |
|---|---|
| "What are my rights if my landlord refuses to return my security deposit?" | RAG retrieves rent control act sections → simplified answer |
| "என் கணவர் என்னை அடிக்கிறார், நான் என்ன செய்வது?" | Detects Tamil → retrieves DV Act → responds in Tamil |
| "Can a consumer file a complaint for defective product?" | Retrieves Consumer Protection Act → plain English answer |
| "What is Section 498A of IPC?" | Direct section retrieval → simplified explanation |

---

## ⚠️ Disclaimer

> **This AI provides general legal information and is not a substitute for professional legal advice. Please consult a qualified lawyer for specific legal matters.**

---

## 📜 License

MIT License — Free for educational, hackathon, and government integration use.
