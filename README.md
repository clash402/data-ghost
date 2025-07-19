# Data Ghost 👻

**A natural-language analytics assistant powered by LangChain, FastAPI, and ChromaDB**

> *It’s the ghost in your spreadsheet.* 🕵️‍♂️

&#x20;

---

## 💥 Real-World Use Case

> Upload a messy spreadsheet, ask “What changed last quarter?” — and get a clear summary in seconds.

---

## 🧠 What It Does

**Data Ghost** lets you ask questions about your data—using plain English.\
Upload a CSV file, and get meaningful answers back instantly, without writing a single line of code.

It can summarize, analyze, and explain CSVs, spreadsheets, or pasted data using conversational AI—with optional RAG support for contextual lookup.

Example:

> *"What was the average revenue in Q2?"*\
> *"Show me the top 5 products by return rate."*

Behind the scenes, it combines embeddings, retrieval, and LLM-powered reasoning to help you understand your data—fast.

---

## 🚀 Why It Matters

Even in data-rich environments, accessing insights often requires technical expertise.\
**Data Ghost** lowers that barrier by turning questions into queries—making data exploration accessible, fast, and natural.

It's designed as a lightweight, modular assistant built to embed inside your dashboard, BI tool, or next-gen SaaS.

---

## 📈 Benefits

- Ask questions like a human and get insights like an analyst
- No formulas, no coding. Just fast, useful answers
- Grounded context with RAG support for deeper understanding
- Transparent usage—know what it costs, line by line

---

## 🔁 Flow Diagram

(Visual diagram in progress—will show X → Y → Z)

---

## 📜 Agent Log

Coming soon...

---

## 🧠 RAG Support

Optional RAG module lets you pull insights from uploaded reference material (PDFs, docs, etc.) to ground responses in real context. Ideal for spreadsheets that depend on business logic or supplementary documentation.

---

## 🔐 Guardrails & Safety

To prevent abuse and control OpenAI API costs during demos:

- Requests are **rate-limited** on the backend (per-IP cooldown)
- Each query uses a safe `max_tokens` setting
- Optional environment config supports **demo mode** with mock responses

---

## 💸 Token Cost Display

Includes per-request token usage and estimated cost for transparency.

```bash
[INFO] Prompt tokens: 355
[INFO] Completion tokens: 841
[INFO] Estimated cost: $0.0162
```

---

## 📦 Reusability

The core modules (embedding, retrieval, querying) are designed to be reused across AI-powered apps. This project serves as both a demo and a foundation for more advanced agentic data tools.

---

## 🛠️ Tech Stack

- ****Frontend:**** Next.js, Tailwind CSS, React Query
- ****Backend:**** FastAPI (tool interfaces + execution logic)
- ****AI Framework:**** LangChain (retrieval + prompt chains)
- ****Storage:**** ChromaDB
- ****LLM:**** OpenAI (can be swapped for open-source models)
- ****Deployment:**** Vercel (frontend) + Fly.io (backend)

---

## 🔑 Requirements

You’ll need API keys for:

- OpenAI (for embeddings and reasoning)

---

## 💪 Setup

```bash
# clone the repo
git clone https://github.com/yourusername/data-ghost.git
cd data-ghost

# set up environment variables
cp .env.example .env

# install dependencies
pip install -r requirements.txt
npm install

# run backend
uvicorn backend.main:app --reload

# run frontend
npm run dev
```

---

## 🧑‍💻 Built By

Josh Courtney – Senior Full Stack Engineer\
[JoshCourtney.com](https://joshcourtney.com) | [LinkedIn](https://www.linkedin.com/in/joshcourtney402/)

