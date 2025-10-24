# DistanceProgram
### Docker run 
docker compose up --build
http://localhost:8000

# Project Information
# 🛰️ DistanceChallenge

A full-stack web application that calculates driving distance between two locations, stores query history, and displays past results in a clean modern UI.

Built with:
- **FastAPI** — Backend REST API (deployed on Heroku)
- **PostgreSQL** — Persistent storage for query history
- **SvelteKit** — Frontend interface (deployed on Vercel)
- **SQLAlchemy** — ORM for structured database access
- **Nominatim (OpenStreetMap)** — Geocoding and distance lookup

---

## 🚀 Project Overview

**DistanceChallenge** allows users to:
1. Enter two addresses (source + destination).
2. Receive both kilometer and mile distances using the Haversine formula.
3. View a table of previous lookups (stored in PostgreSQL).
4. Rate-limited backend to prevent abuse.
5. Simple, clean SvelteKit interface.

---

Frontend and backend are decoupled but communicate via REST.

---

## ⚙️ Environment Variables

| Variable | Description | Example |
|-----------|--------------|----------|
| `ENV` | Application environment | `production` |
| `DATABASE_URL` | Set by Heroku Postgres | *(auto-injected)* |
| `SQLALCHEMY_DATABASE_URL` | Normalized connection string | `postgresql+psycopg://...` |
| `CORS_ORIGINS` | Allowed frontend origins | `https://distance-ui.vercel.app,http://localhost:5173` |
| `SECRET_KEY` | For session/JWT signing | `your_secret_here` |
| `RATE_LIMIT_MAX_REQUESTS` | Requests per window | `60` |
| `RATE_LIMIT_WINDOW_SECONDS` | Window in seconds | `60` |
| `NOMINATIM_USER_AGENT` | User agent for geocoder | `distance-app-your@email.com` |

---

## 💻 Local Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 16+
- (Optional) Docker & Docker Compose

### Frontend
cd frontend
npm install
npm run dev

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

