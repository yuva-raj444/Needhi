# NyayaSahaya — Project Architecture & Technology Stack

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│                    (http://localhost:3000)                      │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  React 18 Frontend (SPA)                                │  │
│  │  - ChatInterface (RAG Q&A)                              │  │
│  │  - ClassifierPanel (Issue classification)              │  │
│  │  - ComplaintForm (Draft generator)                     │  │
│  │  - DocumentUpload (RAG indexing)                       │  │
│  │  - Language support (EN/TA)                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ▲                                     │
│                           │                                     │
│                      REST API                                   │
│                    (Axios client)                               │
│                           │                                     │
│                           ▼                                     │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │
                HTTP (Port 8000)
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                FastAPI Backend (Python 3.11)                    │
│                (http://localhost:8000)                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Router Layer                                           │  │
│  │  - /api/query/ (RAG Q&A)                               │  │
│  │  - /api/classify/ (Issue classifier)                   │  │
│  │  - /api/complaint/ (Draft + PDF)                       │  │
│  │  - /api/documents/ (Upload + indexing)                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Service Layer (Business Logic)                         │  │
│  │                                                          │  │
│  │  ┌────────────────┐    ┌──────────────────┐            │  │
│  │  │ RAGService     │    │ ClassifierService│            │  │
│  │  │ - Retrieval    │    │ - LLM classify   │            │  │
│  │  │ - Augmentation │    │ - 6 categories   │            │  │
│  │  │ - Generation   │    │ - Confidence     │            │  │
│  │  └────────────────┘    └──────────────────┘            │  │
│  │                                                          │  │
│  │  ┌──────────────┐    ┌─────────────────┐              │  │
│  │  │ Complaint    │    │ Language        │              │  │
│  │  │ Service      │    │ Service         │              │  │
│  │  │ - LLM draft  │    │ - Detect (EN/TA)│              │  │
│  │  │ - PDF export │    │ - Translate     │              │  │
│  │  └──────────────┘    └─────────────────┘              │  │
│  │                                                          │  │
│  │  ┌─────────────────────────────────────┐              │  │
│  │  │ Supporting Services                 │              │  │
│  │  │ - LLMService (OpenAI wrapper)       │              │  │
│  │  │ - EmbeddingService (FAISS vector)   │              │  │
│  │  │ - PDFService (fpdf2 generator)      │              │  │
│  │  └─────────────────────────────────────┘              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Data Layer                                             │  │
│  │                                                          │  │
│  │  ┌─────────────────────┐    ┌─────────────────────┐   │  │
│  │  │  FAISS Vector Store │    │ Sample Legal Docs   │   │  │
│  │  │  - Embeddings       │    │ - IPC_Sample.txt    │   │  │
│  │  │  - Chunks (125+)    │    │ - Consumer_*.txt    │   │  │
│  │  │  - Metadata         │    │ - Domestic_*.txt    │   │  │
│  │  │  - Index file       │    │ - Tenancy_*.txt     │   │  │
│  │  └─────────────────────┘    └─────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ▼                                     │
└─────────────────────────────────────────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  OpenAI API  │  │ File Storage │  │ Environment  │
    │  - GPT-4     │  │ - .txt files │  │ - .env vars  │
    │  - Embedding │  │ - FAISS idx  │  │ - CORS rules │
    │  - API calls │  │ - PDFs       │  │ - API keys   │
    └──────────────┘  └──────────────┘  └──────────────┘
```

---

## 🛠️ Technology Stack

### **Backend**

| Component | Technology | Purpose |
|---|---|---|
| **Framework** | FastAPI 0.110+ | REST API, async support |
| **Language** | Python 3.11+ | Core language |
| **LLM** | OpenAI GPT-4 | Legal reasoning, classification |
| **Embeddings** | text-embedding-3-small | Vector representations |
| **Vector DB** | FAISS | Fast similarity search |
| **Text Processing** | LangChain | Chunking, text splitting |
| **PDF Generation** | fpdf2 | Complaint letter PDFs |
| **Language Detection** | langdetect | EN/TA auto-detection |
| **Web Server** | Uvicorn | ASGI server |
| **Environment** | python-dotenv | Config management |
| **Validation** | Pydantic v2 | Request/response schemas |

### **Frontend**

| Component | Technology | Purpose |
|---|---|---|
| **Framework** | React 18 | SPA, component-based UI |
| **Language** | JavaScript (ES6+) | Frontend logic |
| **HTTP Client** | Axios | API requests with timeout |
| **Styling** | CSS3 | Responsive design |
| **Fonts** | Google Fonts | Multi-language typography |
| **Build Tool** | Create React App | Build & development |
| **Package Manager** | npm | Dependency management |
| **Design System** | Custom CSS Variables | Consistent theming |

### **Infrastructure**

| Component | Technology | Purpose |
|---|---|---|
| **Containerization** | Docker | Consistent environments |
| **Orchestration** | Docker Compose | Multi-container setup |
| **Version Control** | Git | Source code management |
| **Deployment** | Render, Netlify, AWS EC2 | Cloud hosting |
| **API Documentation** | Swagger UI / OpenAPI | Interactive API docs |

---

## 🔄 Data Flow Diagrams

### **Diagram 1: RAG Q&A Flow**

```
User Query (EN/TA)
       │
       ▼
[Language Detection]
       │
       ├─ Tamil? → [Translate to English for retrieval]
       └─ English? → [Use as-is]
       │
       ▼
[FAISS Search]
       │
       └─ Retrieve top-5 relevant chunks from vector store
       │
       ▼
[Context Assembly]
       │
       └─ Combine retrieved chunks with section metadata
       │
       ▼
[RAG LLM Generation]
       │
       ├─ System: "Use context, explain simply, cite sections"
       ├─ User: "[Query] Based on: [context]"
       └─ LLM: [Simplified answer in user's language]
       │
       ▼
Formatted Response
├─ Answer (1-2 paragraphs)
├─ Detected Language
├─ Category (if identifiable)
├─ Source Documents (with scores)
└─ Disclaimer
```

### **Diagram 2: Complaint Generation Flow**

```
User Inputs
├─ Name, Address
├─ Opponent name
├─ Issue description
├─ Location, Date
└─ Language preference
       │
       ▼
[Validation]
       │
       └─ All fields filled? Continue : Error
       │
       ▼
[Template Selection]
       │
       ├─ English → COMPLAINT_PROMPT_EN
       └─ Tamil → COMPLAINT_PROMPT_TA
       │
       ▼
[LLM Generation]
       │
       └─ Generate formal legal complaint with:
          ├─ Proper addressing
          ├─ Section references
          ├─ Formal language
          └─ Prayer for relief
       │
       ▼
[Format Selection]
       │
       ├─ Draft View → Display as text
       └─ PDF Download → Convert via fpdf2
       │
       ▼
Output
├─ Draft text (editable)
└─ PDF file (downloadable)
```

### **Diagram 3: Document Indexing Flow**

```
Document Upload (txt/pdf)
       │
       ▼
[File Validation]
       │
       └─ .txt or .pdf? Continue : Error
       │
       ▼
[Text Extraction]
       │
       ├─ .txt → Read directly
       └─ .pdf → PyPDF2 extraction
       │
       ▼
[Text Chunking]
       │
       └─ RecursiveCharacterTextSplitter
          ├─ Size: 500 words
          ├─ Overlap: 50 words
          └─ Separators: ["\n\n", "SECTION", ". ", " "]
       │
       ▼
[Embedding Generation]
       │
       └─ OpenAI text-embedding-3-small
          ├─ 1536-dimensional vectors
          └─ Batch processing
       │
       ▼
[FAISS Indexing]
       │
       ├─ Add vectors to IndexFlatL2
       ├─ Store metadata (source, text, index)
       └─ Save to disk
       │
       ▼
[Status Response]
├─ Documents processed
├─ Total chunks created
└─ Vector count
```

---

## 📊 Data Models

### **Request/Response Schemas**

```python
# Query Request
{
  "question": str,           # 3-2000 chars
  "language": Optional[str]  # "en" or "ta"
}

# Query Response
{
  "answer": str,
  "detected_language": str,
  "category": Optional[str],
  "sources": List[SourceChunk],
  "disclaimer": str
}

# Classify Request
{
  "description": str  # 5-3000 chars
}

# Classify Response
{
  "category": str,           # Criminal, Civil, Family, Consumer, Land, Welfare
  "confidence": str,         # High, Medium, Low
  "explanation": str,
  "detected_language": str,
  "disclaimer": str
}

# Complaint Request
{
  "complainant_name": str,
  "complainant_address": str,
  "opponent_name": str,
  "issue_description": str,
  "location": str,
  "date": str,               # YYYY-MM-DD
  "language": Optional[str]  # "en" or "ta"
}

# Complaint Response
{
  "draft_text": str,
  "language": str,
  "disclaimer": str
}
```

---

## 🗄️ Database & Storage

### **FAISS Index Structure**

```
index.faiss (Binary format)
├─ Number of vectors: 125+ (from 4 sample docs)
├─ Dimension: 1536 (text-embedding-3-small)
├─ Distance metric: L2 (Euclidean)
└─ Index type: IndexFlatL2

metadata.pkl (Pickle format)
├─ Vector 0: {"text": "...", "source": "IPC_Sample.txt", "index": 0}
├─ Vector 1: {"text": "...", "source": "Consumer_Protection_Act.txt", "index": 1}
├─ Vector 2: {"text": "...", "source": "Domestic_Violence_Act.txt", "index": 2}
└─ ...
└─ Vector 124: {"text": "...", "source": "Tenancy_Rights.txt", "index": 124}
```

### **File Organization**

```
backend/app/data/
├── vector_store/
│   ├── index.faiss         # Binary FAISS index
│   └── metadata.pkl        # Chunk metadata
└── sample_docs/
    ├── IPC_Sample.txt
    ├── Consumer_Protection_Act.txt
    ├── Domestic_Violence_Act.txt
    └── Tenancy_Rights.txt
```

---

## ⚡ Performance Characteristics

| Operation | Latency | Bottleneck |
|---|---|---|
| **RAG Query** | 2-5s | Embedding generation (1s) + LLM call (1-3s) |
| **Classifier** | 1-2s | LLM call only |
| **Complaint Draft** | 2-4s | LLM generation time |
| **FAISS Search** | <100ms | In-memory operation |
| **Embedding** | ~1s | OpenAI API call |
| **PDF Generation** | <500ms | Local fpdf2 processing |

---

## 🔐 Security Considerations

| Aspect | Implementation |
|---|---|
| **API Keys** | Stored in .env (never in code) |
| **CORS** | Whitelist frontend origins in config |
| **Input Validation** | Pydantic schemas enforce types/lengths |
| **Rate Limiting** | Can add Redis ratelimit middleware |
| **HTTPS** | Enable in production (via reverse proxy) |
| **Authentication** | Not required (public legal aid) |
| **Data Privacy** | No data stored between requests |

---

## 🚀 Scalability Notes

### Current Limits
- **FAISS Index Size:** 1-2GB max (in-memory)
- **Concurrent Users:** ~10-20 (single instance)
- **QPS:** ~5 requests/second (GPT-4 rate limit)

### To Scale
1. **Multi-instance backend** → Load balance with nginx
2. **Database FAISS** → Use Milvus/Pinecone instead
3. **Caching layer** → Redis for embedding cache
4. **Async jobs** → Celery for long-running tasks
5. **CDN frontend** → Cloudflare for static assets

---

## 📦 Dependency Tree (Simplified)

```
Backend Dependencies
├── openai (LLM & embeddings)
├── fastapi (REST framework)
│   └── pydantic (validation)
├── faiss-cpu (vector search)
├── langchain (text processing)
├── langdetect (language detection)
├── fpdf2 (PDF generation)
└── python-dotenv (env management)

Frontend Dependencies
├── react (UI framework)
├── axios (HTTP client)
├── lucide-react (icons - optional)
└── react-scripts (build tools)
```

---

## 🧪 Testing Matrix

| Component | Unit Tests | Integration Tests |
|---|---|---|
| RAG Service | ✅ Mock LLM/FAISS | ✅ E2E query flow |
| Classifier | ✅ Mock LLM | ✅ Category detection |
| Complaint | ✅ Draft generation | ✅ PDF export |
| Language | ✅ Detection logic | ✅ Translation flow |
| Embeddings | ✅ Mock OpenAI | ✅ Index operations |

---

## 🎯 Key Design Decisions

1. **FAISS over cloud vector DB:** Faster, works offline, free
2. **GPT-4 over open models:** Accuracy matters for legal domain
3. **FastAPI over Flask:** Better async, auto-docs, validation
4. **React SPA over templates:** Modern UX, responsive design
5. **Stateless architecture:** Easy horizontal scaling
6. **No database:** Only file-based persistence (portable)

