import re

# Allow-list: letters, numbers, spaces, commas, periods, hyphens, #
SAFE_RE = re.compile(r"^[\w\s,#\.-]{3,255}$")

def is_safe(addr: str) -> bool:
    return bool(SAFE_RE.match(addr))
