# NyayaSahaya — Deployment Guide

## 🚀 Quick Local Setup

### 1. Clone & Setup Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Index Sample Documents

Before starting the server, you can pre-index the sample documents:

```bash
# Place .txt or .pdf files in backend/app/data/sample_docs/
# Then start the server and call:
# POST http://localhost:8000/api/documents/index-all
```

### 3. Start Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be live at: **http://localhost:8000**
API docs: **http://localhost:8000/docs**

### 4. Start Frontend

```bash
cd frontend
npm install
npm start
```

Frontend will open at: **http://localhost:3000**

---

## 🐳 Docker Setup

```bash
# From project root
docker-compose up --build

# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Backend API Docs: http://localhost:8000/docs
```

To stop:
```bash
docker-compose down
```

---

## ☁️ Cloud Deployment

### Option 1: Render.com

#### Backend Deployment

1. **Create Render Account** → https://render.com
2. **Connect GitHub Repo**
3. **Create Web Service**:
   - Name: `nyayasahaya-backend`
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Root Directory: `backend`
4. **Add Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI key
   - `OPENAI_MODEL`: `gpt-4`
   - `CORS_ORIGINS`: Frontend URL (e.g., `https://nyayasahaya.netlify.app`)
5. **Deploy** → Takes ~5 min

Backend URL: `https://nyayasahaya-backend.onrender.com`

#### Frontend Deployment

1. **Connect same GitHub repo to Netlify** → https://netlify.com
2. **Build Settings**:
   - Build command: `npm run build`
   - Publish directory: `frontend/build`
3. **Environment Variables**:
   - `REACT_APP_API_URL`: `https://nyayasahaya-backend.onrender.com`
4. **Deploy** → Takes ~3 min

Frontend URL: `https://nyayasahaya.netlify.app`

---

### Option 2: AWS + EC2

1. **Create EC2 instance** (Ubuntu 22.04, t2.micro free tier)
2. **SSH into instance**:
   ```bash
   ssh -i your-key.pem ubuntu@<instance-ip>
   ```
3. **Install Docker & Docker Compose**:
   ```bash
   sudo apt update && sudo apt install -y docker.io docker-compose
   sudo systemctl start docker
   sudo usermod -aG docker ubuntu
   ```
4. **Clone repo & deploy**:
   ```bash
   git clone https://github.com/yourusername/niral.git
   cd niral
   docker-compose up -d
   ```
5. **Setup SSL** (Let's Encrypt):
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   ```

---

### Option 3: Heroku (Legacy - Using containers)

```bash
heroku login
heroku create nyayasahaya
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku config:set OPENAI_API_KEY=your_key
```

---

## 📋 Environment Variables Checklist

**Backend (.env)**:
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
CORS_ORIGINS=http://localhost:3000,https://frontend-url.com
FAISS_INDEX_PATH=app/data/vector_store/index.faiss
```

**Frontend (.env or Netlify)**:
```
REACT_APP_API_URL=http://localhost:8000  # or https://api-url.com
```

---

## ✅ Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:3000
- [ ] Ask a legal question in Chat
- [ ] Classifier returns a category
- [ ] Can generate complaint draft
- [ ] Can upload and index documents
- [ ] Language toggle works (EN ↔ TA)
- [ ] Disclaimer appears on page

---

## 🔧 Troubleshooting

### **Backend starts but no AI responses**
- ✓ Check `.env` has valid `OPENAI_API_KEY`
- ✓ Check `gpt-4` access in your OpenAI account
- ✓ Try a simpler query first

### **CORS errors in browser console**
- ✓ Backend's `CORS_ORIGINS` must include frontend URL
- ✓ Restart backend after changing `.env`

### **No documents in index**
- ✓ Place .txt/.pdf files in `backend/app/data/sample_docs/`
- ✓ Call `POST /api/documents/index-all` via browser/Postman
- ✓ Wait for indexing to complete

### **Slow response on first query**
- ✓ Normal - embedding generation takes 2-3 seconds
- ✓ Subsequent queries will be faster

### **Frontend can't reach backend**
- ✓ Check `REACT_APP_API_URL` is correct
- ✓ Backend should be running
- ✓ Check firewall settings

---

## 📊 Performance Tips

1. **Index only critical sections** to reduce latency
2. **Use GPT-3.5-turbo** for faster (but less accurate) responses
3. **Enable FAISS GPU acceleration** for large indexes
4. **Cache responses** on frontend with Redis
5. **Use CDN** for frontend assets (Cloudflare, AWS CloudFront)

---

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/yourusername/niral/issues
- Email: support@nyayasahaya.com
- Discord: [Link to community]

