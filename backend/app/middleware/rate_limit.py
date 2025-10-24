# backend/app/middleware/rate_limit.py
import time
from collections import defaultdict, deque
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

WINDOW_SECONDS = 60
MAX_REQUESTS = 30

_hits = defaultdict(deque)

def allow(ip: str) -> bool:
    now = time.time()
    q = _hits[ip]
    # drop stale timestamps
    while q and now - q[0] > WINDOW_SECONDS:
        q.popleft()
    if len(q) >= MAX_REQUESTS:
        return False
    q.append(now)
    return True

LIMITED_PATHS = ("/api/v1/distance", "/distance")

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path.startswith(LIMITED_PATHS):
            ip = request.client.host if request.client else "unknown"
            if not allow(ip):
                return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
        return await call_next(request)
