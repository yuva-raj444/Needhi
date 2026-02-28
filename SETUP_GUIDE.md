# NyayaSahaya — Complete Setup & Usage Guide

## 📖 Table of Contents
1. [Quick Start](#quick-start)
2. [Environment Setup](#environment-setup)
3. [Running Locally](#running-locally)
4. [Docker Deployment](#docker-deployment)
5. [API Documentation](#api-documentation)
6. [Frontend Usage](#frontend-usage)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

**TL;DR - Get running in 5 minutes:**

```bash
# 1. Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# ⚠️ Edit .env and add OPENAI_API_KEY
uvicorn app.main:app --reload

# 2. Frontend (new terminal)
cd frontend
npm install
npm start
```

**Visit:** http://localhost:3000

---

## 🔧 Environment Setup

### Prerequisites

- **Python 3.11+**
  ```bash
  python --version  # Should be 3.11+
  ```

- **Node.js 18+**
  ```bash
  node --version  # Should be 18+
  npm --version   # Should be 9+
  ```

- **OpenAI API Key** (Free trial includes $5 credit)
  - Get it from: https://platform.openai.com/api-keys
  - Models: `gpt-4`, `text-embedding-3-small`

### Optional but Recommended

- **Docker & Docker Compose** (for containerized deployment)
- **Git** (for version control)
- **Postman** (for testing APIs)

---

## 💻 Running Locally

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/niral.git
cd niral
```

### Step 2: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy .env template
cp .env.example .env

# Edit .env and add your OpenAI API key
# Open .env in your editor and change:
# OPENAI_API_KEY=sk-your-actual-key-here
```

**Backend .env example:**
```
OPENAI_API_KEY=sk-proj-abc123xyz789...
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
FAISS_INDEX_PATH=app/data/vector_store/index.faiss
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=5
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Step 3: Index Sample Documents

```bash
# Documents are already in: backend/app/data/sample_docs/
# They include:
# - IPC_Sample.txt (criminal law)
# - Consumer_Protection_Act.txt
# - Domestic_Violence_Act.txt
# - Tenancy_Rights.txt

# You can add more .txt or .pdf files there
```

### Step 4: Start Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Test backend:**
- Health check: http://localhost:8000/health
- API Docs: http://localhost:8000/docs
- Sample query: 
  ```bash
  curl -X POST "http://localhost:8000/api/query/" \
    -H "Content-Type: application/json" \
    -d '{"question":"What is Section 498A IPC?"}'
  ```

### Step 5: Start Frontend

**New terminal window:**

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Expected output:**
```
Compiled successfully!

You can now view nyayasahaya in the browser.

  http://localhost:3000
```

Browser will auto-open to http://localhost:3000

---

## 🐳 Docker Deployment

### Using Docker Compose (Easiest)

```bash
# From project root directory
docker-compose up --build

# On first run, wait 60-90 seconds for images to build
# Then visit:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

To stop:
```bash
docker-compose down
```

### Manual Docker Build

**Backend:**
```bash
cd backend
docker build -t nyayasahaya-backend .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key \
  nyayasahaya-backend
```

**Frontend:**
```bash
cd frontend
docker build -t nyayasahaya-frontend .
docker run -p 3000:3000 \
  -e REACT_APP_API_URL=http://localhost:8000 \
  nyayasahaya-frontend
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### 1. Ask Legal Question (RAG)

**Endpoint:**
```
POST /api/query/
```

**Request:**
```json
{
  "question": "What are my rights if my landlord refuses to return security deposit?",
  "language": null
}
```

**Response:**
```json
{
  "answer": "Under the Transfer of Property Act, security deposit must be returned within 30 days...",
  "detected_language": "en",
  "category": "Land",
  "sources": [
    {
      "text": "Security deposit is held in trust for the tenant...",
      "source": "Tenancy_Rights.txt",
      "score": 0.45
    }
  ],
  "disclaimer": "⚠️ This AI provides general legal information..."
}
```

### 2. Classify Legal Issue

**Endpoint:**
```
POST /api/classify/
```

**Request:**
```json
{
  "description": "My husband beats me and doesn't let me work. I want to leave him."
}
```

**Response:**
```json
{
  "category": "Family",
  "confidence": "High",
  "explanation": "This describes domestic violence and seeking divorce protection under DV Act 2005.",
  "detected_language": "en",
  "disclaimer": "⚠️ This AI provides general legal information..."
}
```

### 3. Generate Complaint Draft

**Endpoint:**
```
POST /api/complaint/draft
```

**Request:**
```json
{
  "complainant_name": "Rajesh Kumar",
  "complainant_address": "123, Gandhi Street, Chennai-600001",
  "opponent_name": "ABC Pvt Ltd",
  "issue_description": "Sold defective refrigerator, refuses refund",
  "location": "Chennai, Tamil Nadu",
  "date": "2024-02-20",
  "language": "en"
}
```

**Response:**
```json
{
  "draft_text": "TO THE DISTRICT CONSUMER PROTECTION AUTHORITY, CHENNAI\n\nCOMPLAINT UNDER SECTION 60 OF CONSUMER PROTECTION ACT, 2019\n\nFrom: Rajesh Kumar...",
  "language": "en",
  "disclaimer": "⚠️ This AI provides general legal information..."
}
```

### 4. Download Complaint as PDF

**Endpoint:**
```
POST /api/complaint/pdf
```

**Same request as draft** → Returns PDF file

### 5. Upload Document

**Endpoint:**
```
POST /api/documents/upload
```

**Form Data:**
```
file: [binary file content]
```

**Response:**
```json
{
  "message": "Successfully indexed IPC_New.txt",
  "filename": "IPC_New.txt",
  "chunks_created": 45
}
```

### 6. Index All Documents

**Endpoint:**
```
POST /api/documents/index-all
```

**Response:**
```json
{
  "message": "Successfully indexed all documents",
  "documents_processed": 4,
  "total_chunks": 125
}
```

### 7. Check Index Status

**Endpoint:**
```
GET /api/documents/status
```

**Response:**
```json
{
  "total_vectors": 125,
  "total_metadata": 125,
  "index_loaded": true,
  "documents_on_disk": ["IPC_Sample.txt", "Consumer_Protection_Act.txt", "Domestic_Violence_Act.txt", "Tenancy_Rights.txt"]
}
```

### 8. Health Check

**Endpoint:**
```
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 🎨 Frontend Usage

### Tab 1: Ask Legal Question

1. **Enter your question** in Tamil or English
2. **Click "Send"** or press Enter
3. **System automatically detects language**
4. **Get simplified answer with source documents**

**Example questions:**
- "What is Section 498A?"
- "என் குடியாண்மையின் உரிமைகள் என்ன?"
- "How do I file a consumer complaint?"

### Tab 2: Classify Legal Issue

1. **Describe your legal situation** (5-500 words)
2. **Click "Classify Issue"**
3. **See category with confidence level**

**Output categories:**
- 🔴 **Criminal** - Crimes, FIR
- 🔵 **Civil** - Contracts, disputes
- 💜 **Family** - Divorce, custody
- 🟢 **Consumer** - Product defects, refunds
- 🟤 **Land** - Property, tenancy
- 🟠 **Welfare** - Government schemes, labor

### Tab 3: Draft Complaint

1. **Fill in your details:**
   - Your name & address
   - Opponent's name
   - Issue description
   - Incident location & date
2. **Choose language** (EN or TN)
3. **Click "Generate Draft"**
4. **View draft or download as PDF**

### Tab 4: Upload Documents

1. **Drag & drop** .txt or .pdf files
2. **Or click to browse** your computer
3. **System auto-chunks and indexes**
4. **See indexing status**

**Supported formats:**
- Plain text (.txt) - ✅ Best
- PDF (.pdf) - ✅ Also supported

---

## 🌐 Language Support

### Supported Languages
- **English (EN)** - Full support
- **Tamil (TA)** - Full support

### Auto-Detection
The system automatically detects language from:
1. User input text
2. Chat messages
3. Classifier descriptions

### Manual Override
Use `language` parameter in API:
```json
{
  "question": "என் கேள்வி",
  "language": "ta"
}
```

---

## 📊 API Testing

### Using cURL

```bash
# Test RAG Q&A
curl -X POST "http://localhost:8000/api/query/" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Section 302 IPC?"}'

# Test Classifier
curl -X POST "http://localhost:8000/api/classify/" \
  -H "Content-Type: application/json" \
  -d '{"description":"Someone stole my phone"}'

# Test Upload
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@backend/app/data/sample_docs/IPC_Sample.txt"
```

### Using Postman

1. **Import** the API docs from `http://localhost:8000/openapi.json`
2. **Create requests** for each endpoint
3. **Test with different inputs**
4. **Debug response times**

---

## ⚙️ Configuration

### Backend Settings (.env)

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-...              # Your API key (required)
OPENAI_MODEL=gpt-4                 # Model: gpt-4 or gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# FAISS Vector Store
FAISS_INDEX_PATH=app/data/vector_store/index.faiss

# Text Chunking
CHUNK_SIZE=500                     # Words per chunk
CHUNK_OVERLAP=50                   # Words of overlap

# Retrieval
TOP_K_RESULTS=5                    # Documents to retrieve

# CORS
CORS_ORIGINS=http://localhost:3000  # Allowed frontend URLs
```

### Frontend Settings (.env)

```bash
REACT_APP_API_URL=http://localhost:8000  # Backend URL
```

---

## 🐛 Troubleshooting

### Problem: "CORS error in browser"

**Solution:**
```bash
# Edit backend/.env and add frontend URL to CORS_ORIGINS
CORS_ORIGINS=http://localhost:3000,https://your-frontend.com

# Restart backend
```

### Problem: "No response from API"

**Checklist:**
- [ ] Backend is running (`http://localhost:8000/health`)
- [ ] `OPENAI_API_KEY` is valid in `.env`
- [ ] Network connectivity is OK
- [ ] Check backend logs for errors

### Problem: "Empty response / No sources"

**Solution:**
```bash
# Index the sample documents
# 1. Via UI: Go to "Upload Documents" tab → Click "Re-index All Documents"
# 2. Via API: curl -X POST "http://localhost:8000/api/documents/index-all"
# 3. Check status: curl "http://localhost:8000/api/documents/status"
```

### Problem: "Slow responses"

**This is normal:**
- First query: 3-5 seconds (embedding generation)
- Subsequent queries: 1-2 seconds (cached embeddings)

**To improve:**
1. Use GPT-3.5-turbo instead of GPT-4 (in `.env`)
2. Reduce `TOP_K_RESULTS` to 3
3. Add FAISS GPU support (advanced)

### Problem: "Frontend not connecting to backend"

**Check:**
```bash
# 1. Backend is running
curl http://localhost:8000/health

# 2. REACT_APP_API_URL is set in frontend
# Open frontend/.env or check Network tab in browser DevTools

# 3. Check browser console for errors (F12)
```

### Problem: "PDF download not working"

**Solution:**
- Use Chrome/Firefox (not Safari)
- Check browser pop-up blocker settings
- Try downloading in incognito mode

### Problem: "Tamil text appears as boxes"

**Solution:**
1. **Frontend:** Fonts are auto-loaded from Google Fonts
2. **PDF:** Limited Tamil font support (falls back to Latin)
3. **To fix:** Install Noto Sans Tamil font locally

---

## 📈 Performance Tips

### For Better Accuracy:
1. **Ask specific questions** - "What is Section 498A?" vs "Tell me about laws"
2. **Provide context** - Include dates, names, amounts
3. **Use both languages** - Let system auto-detect
4. **Reference sections** - System retrieves more accurately with act names

### For Faster Response:
1. Use `GPT-3.5-turbo` (faster but less accurate)
2. Reduce `TOP_K_RESULTS` to 3 in `.env`
3. Pre-index critical sections only
4. Use local GPU for embeddings (advanced)

---

## 📚 Additional Resources

- **Legal Database:** [DadaBhaiForgetter](https://indiankanoon.org) - Case law search
- **OpenAI Docs:** https://platform.openai.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **React Docs:** https://react.dev

---

## 🆘 Getting Help

### Debug Logs

**Backend logs:**
```bash
# Set log level
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload
```

**Frontend logs:**
```bash
# Open browser DevTools (F12)
# Go to Console tab
# Watch for red errors
```

### Report Issues

1. **GitHub Issues:** https://github.com/yourusername/niral/issues
2. **Email:** support@nyayasahaya.com
3. **Discord:** [Community link]

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Backend starts without errors
- [ ] `http://localhost:8000/docs` opens (Swagger UI)
- [ ] Frontend loads at `http://localhost:3000`
- [ ] Can ask a question and get response
- [ ] Classifier works
- [ ] Can generate complaint draft
- [ ] Can upload documents
- [ ] Language toggle works
- [ ] Disclaimer is visible
- [ ] All tabs are accessible

**If all checks pass, you're ready to deploy!** 🚀
