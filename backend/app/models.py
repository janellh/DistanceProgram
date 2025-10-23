from sqlalchemy import Column, Integer, String, Float, DateTime, text
from .db import Base

class QueryRecord(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)
    source_raw = Column(String(255), nullable=False)
    dest_raw = Column(String(255), nullable=False)
    source_lat = Column(Float, nullable=False)
    source_lon = Column(Float, nullable=False)
    dest_lat = Column(Float, nullable=False)
    dest_lon = Column(Float, nullable=False)
    distance_km = Column(Float, nullable=False)
    distance_mi = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("NOW()"))
