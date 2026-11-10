# ServiceFind

Professional Service Finder mobile application built with **Flutter** (mobile
frontend) and **Python FastAPI** (backend REST API), targeting **MongoDB Atlas**,
developed entirely inside **GitHub Codespaces**.

## Repository layout

```
service-finder/
├── .devcontainer/          # GitHub Codespaces dev container (Flutter, Dart,
│                           # Python, Chromium, Git)
├── backend/                # FastAPI REST API
│   ├── app/main.py         # Application factory + ASGI app
│   ├── app/routers/health.py   # GET /health
│   ├── requirements.txt    # Python dependencies
│   ├── tests/              # pytest suite
│   └── .env.example        # Environment variables template
├── mobile/                 # Flutter application
│   ├── lib/main.dart       # Entry point
│   ├── lib/app/            # App shell (theme, routes)
│   ├── lib/features/       # Feature-based modules
│   ├── test/               # Flutter tests
│   └── pubspec.yaml        # Flutter dependencies
├── docs/                   # Architecture, database & API design
│   ├── architecture.md
│   ├── database-design.md
│   └── api-design.md
├── scripts/                # Helper scripts (reserved)
├── .gitignore
└── README.md               # This file
```

## Development environment (GitHub Codespaces)

All tooling runs **inside the Codespace container** — do not install Flutter,
Dart, or Python on your Windows host.

### Reopening / recreating the Codespace

1. Go to `https://github.com/yitayalDev/ServiceFind`
2. Click the green **<> Code** button → **Codespaces** tab →
   **Create codespace on main**.
3. The devcontainer builds automatically: Flutter, Dart, Chromium (Flutter Web),
   Python, and FastAPI dependencies are installed inside the container.
4. Once opened, run the post-create verification:
   ```bash
   bash .devcontainer/post-create.sh
   ```

## Backend (Python FastAPI)

```bash
# 1. Activate the project virtual environment
source /opt/venv/bin/activate

# 2. Install backend dependencies
cd backend
pip install -r requirements.txt

# 3. Copy environment template
cp .env.example .env

# 4. Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Verify the health endpoint (in another terminal)
curl http://localhost:8000/health
# Expected: {"status":"healthy","service":"servicefind-api","version":"0.1.0"}

# 6. Run backend tests
pytest
```

The interactive API docs are available at `http://localhost:8000/docs`.

## Mobile (Flutter)

```bash
# 1. Get Flutter dependencies
cd mobile
flutter pub get

# 2. Analyze the project
flutter analyze

# 3. Run tests
flutter test

# 4. Build for Flutter Web
flutter build web --release

# 5. Run on Chrome (Chromium) - requires CHROME_EXECUTABLE set
flutter run -d chrome
```

## Technology stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Mobile framework | Flutter | 3.47.8 |
| Mobile language | Dart | 3.13.7 |
| Backend framework | FastAPI | 0.162.3 |
| Backend language | Python | 3.14.2 |
| ASGI server | Uvicorn | 0.54.0 |
| Database | MongoDB Atlas | Step 3 |
| Dev environment | GitHub Codespaces devcontainer | — |

## Status

- ✅ Step 1 — Development environment setup (devcontainer, Flutter, Dart,
  Python, FastAPI deps, Chromium)
- ✅ Step 2 — Project architecture + backend & Flutter foundation + docs
- ⏳ Step 3 — MongoDB Atlas connection (planned)
- ⏳ Step 4+ — Feature implementation (auth, services, bookings, ...)

**MongoDB is not configured yet** (planned for Step 3). **Authentication is not
implemented yet.**
