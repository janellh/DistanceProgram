import os
from sqlalchemy import create_engine

raw = os.getenv("SQLALCHEMY_DATABASE_URL") or os.getenv("DATABASE_URL", "")

# Normalize Heroku scheme and ensure SSL
if raw.startswith("postgres://"):
    raw = raw.replace("postgres://", "postgresql+psycopg://", 1)
if "sslmode=" not in raw:
    sep = "&" if "?" in raw else "?"
    raw = f"{raw}{sep}sslmode=require"

engine = create_engine(raw, pool_pre_ping=True)
