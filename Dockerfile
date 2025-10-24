# ---------- Build frontend ----------
FROM node:20-alpine AS fe
WORKDIR /fe
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci || npm i
COPY frontend/ ./
# SvelteKit + Vite build -> /fe/build (contains 200.html and _app/)
RUN npm run build

# ---------- Runtime image (Python + static) ----------
FROM python:3.11-slim AS app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Backend deps
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Backend code
COPY backend/app ./app

# Copy SvelteKit build into /app/static
RUN mkdir -p static
COPY --from=fe /fe/build/ ./static/

# Default envs (overridable via .env/host settings)
ENV DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/distance \
    NOMINATIM_UA=DistanceChallenge/1.0

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

