# ---------- Build frontend ----------
FROM node:20-alpine AS fe
RUN apk add --no-cache libc6-compat
WORKDIR /fe
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --include=dev || npm i --include=dev
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
ENV DATABASE_URL=postgresql://distance_db_user:OvmvDY2sXiyPh5abNXdJjgFM04IloaT9@dpg-d3trn3juibrs73bc2kv0-a/distance_db

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

