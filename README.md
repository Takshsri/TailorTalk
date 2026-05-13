<div align="center">

# 🗂️ TailorTalk AI

**Conversational Google Drive File Discovery Assistant**

*Search your Drive with plain English — no filters, no folders, just ask.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=flat-square)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

</div>

---

## ✨ Overview

TailorTalk AI lets you search your Google Drive using natural language. Instead of manually filtering by file type, date, or folder, simply describe what you're looking for — the AI translates your query into a precise Google Drive API search and returns matching files instantly.

---

## 🚀 Features

- 💬 **Conversational interface** — chat-based file discovery
- 🧠 **LLM-powered query generation** — natural language → Google Drive API query
- 📂 **Rich search support** — search by name, type, content, or date
- ⚡ **Fast responses** — powered by Groq's ultra-low-latency inference
- 🎨 **Modern dark UI** — animated Streamlit frontend with custom CSS
- 🔐 **Service Account auth** — secure Google Drive access via GCP

### Supported Search Types

| Query Type | Example |
|---|---|
| File name | `"Find budget.xlsx"` |
| Partial name | `"Find files with 'invoice' in the name"` |
| File type | `"Show me all PDFs"` |
| Full-text content | `"Find files containing 'quarterly revenue'"` |
| Modified date | `"Files modified this month"` |
| Combined | `"Find spreadsheets with budget modified last week"` |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit + Custom CSS |
| **Backend** | FastAPI |
| **AI / Orchestration** | LangChain |
| **LLM** | Llama 3.3 70B Versatile via Groq |
| **Drive Integration** | Google Drive API v3 |
| **Auth** | Google Service Account (JSON key) |

---

## 📂 Project Structure

```
tailortalk/
│
├── backend/
│   ├── agent.py              # LangChain agent & query generation
│   ├── drive_tool.py         # Google Drive API integration
│   ├── main.py               # FastAPI app & /chat endpoint
│   ├── requirements.txt
│   ├── .env                  # Backend environment variables
│   └── service-account.json  # GCP service account credentials
│
├── frontend/
│   ├── app.py                # Streamlit chat UI
│   ├── requirements.txt
│   └── .env                  # Frontend environment variables
│
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

### Prerequisites

- Python 3.10+
- A Google Cloud Project with Drive API enabled
- A [Groq API key](https://console.groq.com)

---

### 1️⃣ Clone the Repository

```bash
git clone YOUR_GITHUB_REPO_URL
cd tailortalk
```

---

### 2️⃣ Google Drive API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (or select an existing one)
3. Enable the **Google Drive API**
4. Navigate to **IAM & Admin → Service Accounts**
5. Create a Service Account and download the **JSON key**
6. Place the key at `backend/service-account.json`
7. Share your target Google Drive folder with the **service account email**

---

### 3️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:

```env
GROQ_API_KEY=your_groq_api_key
FOLDER_ID=your_google_drive_folder_id
MODEL_NAME=llama-3.3-70b-versatile
FRONTEND_URL=http://localhost:8501
```

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

> Backend runs at: `http://127.0.0.1:8000`

---

### 4️⃣ Frontend Setup

```bash
cd frontend
pip install -r requirements.txt
```

Create a `.env` file in `frontend/`:

```env
BACKEND_URL=http://127.0.0.1:8000
```

Launch the Streamlit app:

```bash
python -m streamlit run app.py
```

> Frontend runs at: `http://localhost:8501`

---

## 🤖 Example Queries

```
Find PDF reports from last week
Show me all images in the folder
Find invoices from vendors
Search for files containing 'budget'
Find spreadsheets modified this month
Locate any QR code images
Find shared documents
```

---

## 🧠 How It Works

```
User Query
    │
    ▼
Streamlit Frontend  ──POST /chat──►  FastAPI Backend
                                          │
                                          ▼
                                    LangChain Agent
                                          │
                              LLM (Llama 3.3 via Groq)
                                          │
                                  Generates Drive query
                                          │
                                          ▼
                                Google Drive API v3
                                          │
                                   Matching Files
                                          │
                                          ▼
                              Streamlit Chat Response
```

1. User enters a natural language query in the chat
2. FastAPI receives it and passes it to the LangChain agent
3. The LLM generates a structured Google Drive API `q` query
4. The Drive API executes the query and returns matching files
5. Results are formatted and streamed back to the chat UI

---

## 🔍 Supported Drive Query Syntax

The AI agent can generate queries using:

- `name contains 'keyword'` — partial filename match
- `name = 'exact-name.pdf'` — exact filename
- `mimeType = 'application/pdf'` — filter by file type
- `fullText contains 'keyword'` — search file contents
- `modifiedTime > '2024-01-01T00:00:00'` — date filtering
- `AND` / `OR` — combined conditions

---

## 🌐 Deployment

### Backend — [Render](https://render.com)

1. Push `backend/` to a GitHub repository
2. Create a new **Web Service** on Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Add environment variables from `.env`
6. Upload `service-account.json` as a secret file

### Frontend — [Streamlit Community Cloud](https://streamlit.io/cloud)

1. Push `frontend/` to a GitHub repository
2. Connect the repo on Streamlit Cloud
3. Set `app.py` as the main file
4. Add `BACKEND_URL` in the Secrets manager

---

## 📸 Screenshots

> *Screenshots will be added after deployment.*

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ using FastAPI, LangChain, Groq, and Streamlit

</div>