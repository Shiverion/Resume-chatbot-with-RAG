# 🧠 Career Conversations Chatbot

A smart conversational agent designed to help users reflect on their career goals, aspirations, and experiences — powered by **Retrieval-Augmented Generation (RAG)** and OpenAI's GPT-4o-mini. Built with ❤️ using lightweight tools like **Gradio**, **OpenAI SDK**, and **ChromaDB**, and managed via the blazing-fast **uv** package manager. 

This project lets users upload their resume and simulate a career conversation — as if you're chatting with an AI version of yourself that actually *knows* what's on your CV. Perfect for personal reflection, mock interviews, or just seeing your experience through a new lens.

---

## 🧘‍♂️ What Kind of Chatbot Is This?

Think of it as a career coach meets your smarter inner voice — thoughtful, slightly cheeky, and deeply curious about your goals. It might ask:

- “What’s one project you’re proud of and why?”
- “What do you value more: impact or income?”
- “Which part of your resume feels the most ‘you’?”

---

## 🚀 What This Project Does

This chatbot acts like a personal career therapist (but less judgmental and always available). It:

- 🧾 Lets you upload your CV (PDF or text) and reads it using `pypdf`
- 🧠 Uses a RAG pipeline with ChromaDB to ground responses in your real experience
- 💬 Simulates conversations using OpenAI's GPT-4o-mini
- ⚙️ Records unanswerable questions and user contact via OpenAI tool-calling and Pushover
- 🧰 Is easily extendable with function calling, agents, or external APIs

---

## 🧩 Core Features

- 🔍 **Context-Aware Chat (RAG)**: Upload your resume, and the bot responds with contextual insights.
- 💬 **LLM-based Conversations**: Uses GPT-4o-mini with multi-step tool calls.
- 📁 **Local File Handling**: Processes `.pdf`, `.txt`, and `.md` files from the `me/` folder.
- ☁️ **Pushover Integration**: Sends push alerts for user interest and unknown questions.
- 🧠 **Cached Embeddings**: Efficient vector search via `hashlib` and `lru_cache` fallback embedding.
- 💻 **Gradio Interface**: Simple and clean interface to talk to the agent.
- ⚡ **UV Environment**: Blazing-fast environment setup with [uv](https://github.com/astral-sh/uv).

---

## 🛠️ How to Use Locally

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/career_conversations.git
cd career_conversations
```

### 2. Set Up the Environment (using uv)

```bash
uv venv
uv pip install -r requirements.txt
```

**Or, if you're starting fresh:**

```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | more"
```
or 
```bash
pip install uv
```

### 3. Sync Dependencies

```bash
uv sync
```
### 4. Prepare Your Documents
Put your files in the /me folder:

    1. Rename your resume to linkedin.pdf
    2. Add a summary of your professional story in summary.txt
    3. Add any supporting files that describe yourself

### 5. Set Up Environment Variables
Create a .env file with your API key

``` env
OPENAI_API_KEY=your_openai_key
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_app_token
```

### 5. Run the app

```bash
uv run app.py
```

## 📝 Folder Structure

career_conversations/
│
├── app.py                     # Main app logic (LLM + RAG chatbot)
├── me/
│   ├── sample_cv.pdf          # CV as PDF source (use yours) (rename it to Linkedin.pdf)
│   └── sample_summary.txt     # Plaintext summary (use yours)
├── requirements.txt
└── README.md


MIT License

Copyright (c) 2025 Muhammad Iqbal Hilmy Izzulhaq