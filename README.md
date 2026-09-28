# Enterprise Log Intelligence Platform

An AI-powered platform for analyzing enterprise logs, investigating incidents, and producing evidence-grounded root-cause reports. It includes a browser interface and a FastAPI backend, with analysis performed by a multi-agent workflow.

## Features

- Upload `.log`, `.csv`, and `.xlsx` files up to 50 MB.
- Parse and normalize events, then analyze severity, reliability, security, and performance signals.
- Correlate findings and produce a root-cause analysis with supporting evidence.
- Retrieve operational knowledge with hybrid search, reranking, and citations.
- Ask follow-up questions about an investigation.
- Authenticate users and save investigations in a SQL database.
- Integrate with GitHub and Gmail when their credentials are configured.
- Evaluate RAG answers through the RAGAS endpoint.

## Technology

- Python 3.12+
- FastAPI and Uvicorn
- SQLAlchemy and PostgreSQL (`psycopg`)
- LangGraph and LangChain
- OpenRouter for language-model access
- Pinecone for vector retrieval
- Pandas and OpenPyXL for CSV and Excel parsing
- HTML, CSS, and JavaScript frontend served by FastAPI

## Project layout

```text
.
├── app/                    # Root import bridge for the src/app package
├── knowledge/
│   ├── dataset/             # Synthetic logs, CSV/XLSX data, RAG documents, evaluations
│   ├── runbooks/            # Operational reference material
│   └── uploads/             # Knowledge files
├── scripts/                # Database, integration, and evaluation scripts
├── src/app/
│   ├── agents/              # Log investigation agents and workflow
│   ├── api/routes/          # FastAPI endpoints
│   ├── auth/                # Authentication and authorization
│   ├── rag/                 # Retrieval and ranking pipeline
│   ├── services/            # Analysis, parsing, chat, and integrations
│   └── static/              # Browser application
├── storage/                 # Local retrieval artifacts
├── uploads/                 # Uploaded log files
├── main.py
├── pyproject.toml
└── uv.lock
```

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- A PostgreSQL database
- API credentials for the integrations you plan to use

## Setup

Clone the repository and install its locked dependencies:

```powershell
git clone https://github.com/Roshannama/Enterprise_log_Intelligence_Platform.git
cd Enterprise_log_Intelligence_Platform
uv sync
```

Create a `.env` file in the repository root. Keep this file private; it is excluded by `.gitignore`.

```dotenv
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/enterprise_logs
JWT_SECRET_KEY=replace-with-a-long-random-secret
OPENROUTER_API_KEY=your-openrouter-api-key

# Required when using Pinecone-backed RAG retrieval
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=your-index-name

# Optional GitHub integration
GITHUB_PERSONAL_ACCESS_TOKEN=your-github-token

# Optional Gmail integration. Provide the credential files separately.
GMAIL_CREDENTIALS_FILE=credentials/gmail_credentials.json
GMAIL_TOKEN_FILE=token.json
```

`DATABASE_URL`, `JWT_SECRET_KEY`, and `OPENROUTER_API_KEY` are needed for the main application features. Pinecone settings are needed for vector retrieval. GitHub and Gmail settings are only needed for those integrations. The Gmail credentials and token files are not included in the repository.

Create the database tables:

```powershell
uv run python scripts/init_db.py
```

Start the application from the repository root:

```powershell
uv run uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) for the web interface. FastAPI's interactive API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/api/auth/login` | Authenticate and receive a bearer token |
| `POST` | `/api/auth/register` | Register a user; requires an administrator token |
| `POST` | `/api/analyze` | Analyze an uploaded `.log`, `.csv`, or `.xlsx` file |
| `GET` | `/api/investigations/{file_id}` | Retrieve a saved investigation |
| `POST` | `/api/chat` | Ask a question about an investigation |
| `POST` | `/api/evaluation/ragas` | Evaluate an answer and its retrieval contexts |

Protected endpoints expect an `Authorization: Bearer <access_token>` header. A successful analysis response includes a `file_id`, which can be used to retrieve the investigation or ask follow-up questions.

Example chat request:

```json
{
  "file_id": "your-file-id",
  "question": "What is the most likely cause of the incident?"
}
```

## Analysis workflow

The upload route validates and stores the file, then dispatches it to the matching parser. Parsed events are sanitized and analyzed for candidate incidents. The LangGraph workflow runs evidence collection and specialist agents, retrieves reference knowledge, correlates findings, checks evidence, assigns severity, and creates the final report.

Supported upload extensions are configured in `src/app/core/config.py`. The current maximum upload size is 50 MB.

## Dataset and evaluation

`knowledge/dataset/` contains synthetic log and tabular examples, RAG reference documents, and expected findings for evaluation. Its README describes the dataset layout and validation details.

Validate the dataset with:

```powershell
uv run python knowledge/dataset/scripts/validate_dataset.py
```

The RAGAS API endpoint is `POST /api/evaluation/ragas`. Additional evaluation and integration utilities are in `scripts/`.

## Security

- Never commit `.env`, provider credentials, or authentication tokens.
- `.gitignore` excludes `.env`, the `credentials/` directory, `token.json`, and virtual-environment files.
- Use a unique, high-entropy `JWT_SECRET_KEY` and keep provider keys in local environment configuration.
- Treat uploaded logs and spreadsheets as potentially sensitive data.
