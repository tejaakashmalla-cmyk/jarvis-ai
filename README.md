# 🤖 AI Smart Chatbot

> **Internship-level Python NLP project** — TF-IDF · Cosine Similarity · NLTK · Streamlit

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=flat-square&logo=streamlit)
![NLTK](https://img.shields.io/badge/NLTK-3.8+-green?style=flat-square)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-orange?style=flat-square&logo=scikit-learn)

---

## 📌 Project Overview

**AI Smart Chatbot** is a production-ready conversational AI application built with Python.
It uses core NLP and ML techniques to understand user messages and return intelligent responses.

### 🚀 Key Features
- ✅ 17 intent categories (greetings, AI, coding, Python, NLP, motivation, jokes, careers & more)
- ✅ TF-IDF Vectorization + Cosine Similarity matching
- ✅ NLTK preprocessing: tokenization, stopword removal, lemmatization
- ✅ Fuzzy spelling correction via `difflib`
- ✅ Session-based chat history
- ✅ Timestamps & confidence scores on every message
- ✅ Dark glassmorphism UI with animated bubbles
- ✅ Sidebar with live stats & tech stack info
- ✅ Typing spinner animation
- ✅ Fallback response for unknown queries
- ✅ Mobile-friendly responsive layout

---

## 📂 Folder Structure

```
ai-chatbot/
│
├── app.py              ← Streamlit frontend (UI, chat logic, session state)
├── chatbot_model.py    ← NLP engine (TF-IDF, cosine similarity, preprocessing)
├── intents.json        ← Training data (17 intents, 150+ patterns)
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
└── assets/             ← (reserved for images/icons)
```

---

## ⚙️ Setup Guide

### 1. Clone or Download

```bash
# If you have git
git clone https://github.com/yourname/ai-chatbot.git
cd ai-chatbot

# Or simply unzip the downloaded folder and cd into it
cd ai-chatbot
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> NLTK data packages (punkt, stopwords, wordnet) are downloaded automatically on first run.

### 4. Run the App

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** 🎉

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this project to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **"New app"**
4. Select your repo, branch (`main`), and set **Main file path** to `app.py`
5. Click **Deploy** — your app is live in ~2 minutes! 🚀

> Make sure `requirements.txt` is in the root of your repo — Streamlit Cloud reads it automatically.

---

## 🧠 How It Works

```
User Input
    │
    ▼
Spelling Correction (difflib)
    │
    ▼
NLP Preprocessing
  • Lowercase & clean
  • Tokenize (NLTK word_tokenize)
  • Remove stopwords (NLTK corpus)
  • Lemmatize (WordNetLemmatizer)
    │
    ▼
TF-IDF Vectorization (scikit-learn)
    │
    ▼
Cosine Similarity vs all training patterns
    │
    ▼
Best Match (score ≥ threshold) → Random response from intent
    OR
Below threshold → Fallback response
```

---

## 📊 Tech Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Frontend | Streamlit | Web UI, session state, layout |
| NLP | NLTK | Tokenization, stopwords, lemmatization |
| Vectorization | scikit-learn TfidfVectorizer | Converts text → numeric vectors |
| Similarity | scikit-learn cosine_similarity | Finds closest matching intent |
| Numerics | NumPy | Array operations |
| Spelling | difflib | Fuzzy word correction |

---

## 🔮 Future Improvements

| Feature | Description |
|---------|-------------|
| 🌐 Web Search | Integrate DuckDuckGo/SerpAPI for live answers |
| 💾 Persistent History | Save chats to SQLite or JSON file |
| 🗣️ Voice Input | Add speech-to-text with `SpeechRecognition` |
| 🧠 Transformer Model | Upgrade to `sentence-transformers` for better embeddings |
| 🌍 Multi-language | Detect and respond in user's language |
| 📊 Analytics Dashboard | Track most asked intents, daily usage |
| 🔐 User Auth | Login system to separate chat histories |
| 🤗 Hugging Face | Plug in a pre-trained QA model (BERT, DistilBERT) |

---

## 👨‍💻 Author

Built with ❤️ using Python, NLTK, scikit-learn & Streamlit.

*Perfect for internship portfolios, college projects & resume showcase.*

---

## 📄 License

MIT License — free to use, modify, and distribute.
