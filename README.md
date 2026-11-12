# Recall AI — Long-Term Memory Assistant

Recall AI is a FastAPI application that saves personal memories, searches them by
semantic similarity, and uses the relevant results to answer questions. It also
supports importing TXT and PDF documents as searchable memory chunks.

## Features

- Create, list, update, and delete user-scoped memories through the API.
- Embed and retrieve relevant memories with Sentence Transformers and Qdrant.
- Generate answers with Gemini and LangGraph.
- Upload TXT and PDF files through the web interface.
- Use a responsive dark-themed chat UI at `/ui/`.
- Evaluate retrieval quality and create a graph from measured evaluation runs.

## Requirements

- Python 3.10 or newer
- PostgreSQL (optional for local development; SQLite is used when
  `DATABASE_URL` is not set)
- Qdrant (optional for local development; an in-memory collection is used when
  `QDRANT_URL` is not set)
- A Gemini API key for AI-generated answers

## Setup

From the project directory, create and activate a virtual environment, then
install dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root. Add the values for the services you
use:

```dotenv
GEMINI_API_KEY=your-gemini-api-key

# Optional: defaults to a local SQLite database.
DATABASE_URL=postgresql://username:password@localhost:5432/long_term_memory

# Optional: defaults to an in-memory Qdrant collection.
QDRANT_URL=https://your-qdrant-instance
QDRANT_API_KEY=your-qdrant-api-key
```

Do not commit `.env` or put real credentials in source control. The local
in-memory Qdrant collection is temporary: its vectors are lost when the process
stops. Configure a Qdrant instance for persistent memory search.

## Run

Start the API and web app:

```powershell
python -m uvicorn app.main:app --reload
```

- Web app: <http://127.0.0.1:8000/ui/>
- API health response: <http://127.0.0.1:8000/>
- Interactive API docs: <http://127.0.0.1:8000/docs>

The database table is created automatically at application startup.

## API overview

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/memories` | Create a memory |
| `GET` | `/memories/{user_id}` | List a user's memories |
| `GET` | `/memory/{memory_id}?user_id={user_id}` | Get one memory |
| `PUT` | `/memory/{memory_id}?user_id={user_id}` | Update a memory |
| `DELETE` | `/memory/{memory_id}?user_id={user_id}` | Delete a memory |
| `POST` | `/chat` | Ask a question using retrieved memories |
| `POST` | `/files/{user_id}` | Upload a TXT or PDF file |

## Retrieval evaluation

`evaluate_memory.py` measures Recall@5, Mean Reciprocal Rank (MRR), and retrieval
latency using the configured database and Qdrant collection. Edit `TEST_CASES`
and `USER_ID` in the script to match memories in your own dataset, then run:

```powershell
python evaluate_memory.py
```

Each successful run appends measured results to
`evaluation/results/history.csv` and updates
`evaluation/results/retrieval_history.png`. The graph plots retrieval-quality
metrics over evaluation runs; latency is printed for each run. These are
retrieval measurements, not end-to-end Gemini response-time benchmarks.

No before/after benchmark data is included: a valid comparison requires running
both versions against the same dataset and evaluation cases. Do not interpret
the graph as a before/after comparison unless that baseline has been collected.

## Project layout

```text
app/
  agent/          LangGraph chat and retrieval
  database/       SQLAlchemy database setup and models
  memory/         Memory, retrieval, and file-processing services
  static/         Web interface
  vector_store/   Qdrant client and collection operations
evaluate_memory.py
requirements.txt
```
