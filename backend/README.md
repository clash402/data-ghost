# Data Ghost Backend API

A FastAPI-based backend for CSV data analysis with AI-powered querying capabilities.

## Features

- **CSV Upload & Processing**: Upload and analyze CSV files
- **AI-Powered Queries**: Ask natural language questions about your data
- **Vector Storage**: ChromaDB integration for semantic search
- **Session Management**: Track conversation history
- **File Management**: Upload, list, and delete files

## Quick Start

### Prerequisites

- Python 3.11+
- uv package manager
- OpenAI API key

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Set up environment variables:
```bash
# Edit .env.local with your API keys
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
DATABASE_URL=sqlite:///./data_ghost.db
CHROMA_DB_PATH=./chroma_db
LOG_LEVEL=INFO
```

3. Run the development server:
```bash
# Option 1: Using the run script
python run.py

# Option 2: Using uv run
uv run python -m src.main

# Option 3: Using uvicorn directly
uv run uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
```

The API will be available at `http://localhost:8080`

## API Endpoints

### Health Check
- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed health with component status

### File Upload
- `POST /upload/` - Upload a CSV file
- `GET /upload/files` - List uploaded files
- `DELETE /upload/files/{file_id}` - Delete a file

### Query
- `POST /ask/` - Ask a question about your data
- `GET /ask/sessions/{session_id}/history` - Get session history
- `DELETE /ask/sessions/{session_id}` - Clear session

## Development

### Running Tests
```bash
uv run pytest
```

### Code Formatting
```bash
uv run black src/
uv run isort src/
```

### Type Checking
```bash
uv run mypy src/
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `ELEVENLABS_API_KEY` | ElevenLabs API key | Optional |
| `DATABASE_URL` | Database connection string | `sqlite:///./data_ghost.db` |
| `CHROMA_DB_PATH` | ChromaDB storage path | `./chroma_db` |
| `UPLOAD_DIR` | File upload directory | `./uploads` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Architecture

The backend follows a clean architecture pattern:

- **Routers**: FastAPI route handlers
- **Services**: Business logic layer
- **Storage**: Data persistence (ChromaDB, file system)
- **Core**: Configuration and logging
- **Utils**: Helper functions
- **Schemas**: Pydantic models for validation 