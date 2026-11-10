# ServiceFind Backend (Python FastAPI)

Backend REST API for the Service Find mobile application.

## Tech stack
- FastAPI — web framework
- Uvicorn — ASGI server
- Pydantic / pydantic-settings — configuration and validation
- PyMongo — MongoDB driver (declared, not connected — Step 3)
- pytest / httpx — testing

## Project layout

```
backend/
├── app/
│   ├── main.py            # FastAPI application factory + ASGI app
│   ├── core/              # configuration, exceptions
│   ├── config/            # (reserved)
│   ├── database/          # MongoDB placeholder (Step 3)
│   ├── models/            # domain models (planned)
│   ├── schemas/           # request/response schemas (planned)
│   ├── routers/           # API route definitions (health defined)
│   ├── services/          # business logic (planned)
│   ├── repositories/      # data access layer (Step 3)
│   ├── middleware/        # custom middleware (planned)
│   └── utils/             # helpers (planned)
├── tests/                 # pytest suite
├── requirements.txt       # Python dependencies
├── .env.example           # environment variables template
└── README.md              # this file
```

## Running locally (inside GitHub Codespaces)

1. Activate the project virtual environment:
   ```bash
   source /opt/venv/bin/activate
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

4. Start the API server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API is available at `http://localhost:8000` and the interactive docs at
   `http://localhost:8000/docs`.

5. Verify the health endpoint:
   ```bash
   curl http://localhost:8000/health
   # Expected: {"status":"healthy","service":"servicefind-api","version":"0.1.0"}
   ```

## Running tests

```bash
cd backend
pytest
```

## Notes
- MongoDB is NOT configured yet (planned for Step 3).
- Authentication is NOT implemented yet.
