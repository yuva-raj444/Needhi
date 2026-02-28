# NyayaSahaya — QUICK START (5 Minutes)

## Step 1: Get OpenAI API Key (2 min)

1. Go to https://platform.openai.com/api-keys
2. Sign up or login
3. Create new API key
4. Copy it (you'll need it)

## Step 2: Clone & Setup Backend (2 min)

```bash
# Navigate to backend
cd backend

# Create Python environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Setup config
cp .env.example .env

# IMPORTANT: Edit .env and add your OpenAI API key
# Open: backend/.env
# Change: OPENAI_API_KEY=sk-your-actual-key-here
```

## Step 3: Start Backend (1 min)

```bash
cd backend
uvicorn app.main:app --reload
```

✅ When you see: `Uvicorn running on http://0.0.0.0:8000`

## Step 4: Start Frontend (in new terminal)

```bash
cd frontend
npm install
npm start
```

✅ Browser opens automatically at http://localhost:3000

## Step 5: Start Using! (Instant)

### Try these:

1. **Chat Tab** → Ask: "What is Section 498A IPC?"
2. **Classifier Tab** → Describe: "My landlord won't return deposit"
3. **Complaint Tab** → Fill form → Generate PDF
4. **Upload Tab** → See sample docs already indexed

---

## 🎯 That's it!

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🆘 Quick Fixes

### Backend won't start
```bash
# Check Python version
python --version          # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend won't connect
- Check backend is running: http://localhost:8000/health
- Check browser console (F12) for errors
- Restart both services

### API returns empty results
- Go to "Upload Documents" tab
- Click "Re-index All Documents"
- Wait ~10 seconds
- Try query again

## 📚 Learn More

- **Full Setup Guide:** [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **Deployment:** [DEPLOYMENT.md](./DEPLOYMENT.md)
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Examples:** [CLASSIFIER_EXAMPLES.md](./CLASSIFIER_EXAMPLES.md)

---

**Ready to help Indian citizens with legal questions!** ⚖️
