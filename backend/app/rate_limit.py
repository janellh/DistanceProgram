import time
from collections import defaultdict

# Token bucket per IP: up to RATE requests per WINDOW seconds, with a BURST.
WINDOW = 60       # seconds
RATE = 60         # tokens per window
BURST = 10        # max burst

class TokenBucket:
    def __init__(self):
        self.last = time.time()
        self.tokens = BURST

    def allow(self) -> bool:
        now = time.time()
        elapsed = now - self.last
        self.last = now

        # Refill based on elapsed time
        self.tokens = min(BURST, self.tokens + elapsed * (RATE / WINDOW))

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

buckets: dict[str, TokenBucket] = defaultdict(TokenBucket)

def allow(ip: str) -> bool:
    return buckets[ip].allow()
