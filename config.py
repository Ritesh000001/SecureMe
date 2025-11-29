import os, secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
PASS_HASH_FILE = DATA_DIR / "pass_hash.json"
SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(24)
