import json, base64, secrets, hashlib, hmac
from pathlib import Path
from functools import wraps
from flask import session, redirect, url_for, flash
from config import PASS_HASH_FILE

SALT_LEN = 16
ITERATIONS = 200_000

def is_master_set() -> bool:
    return PASS_HASH_FILE.exists()

def create_master_passkey(passphrase: str) -> bool:
    salt = secrets.token_bytes(SALT_LEN)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, ITERATIONS)
    data = {
        "salt": base64.b64encode(salt).decode(),
        "hash": hash_bytes.hex(),
        "iterations": ITERATIONS
    }
    PASS_HASH_FILE.write_text(json.dumps(data))
    return True

def verify_master_passkey(passphrase: str) -> bool:
    if not PASS_HASH_FILE.exists():
        return False
    data = json.loads(PASS_HASH_FILE.read_text())
    salt = base64.b64decode(data["salt"])
    expected = bytes.fromhex(data["hash"])
    iters = data.get("iterations", ITERATIONS)
    candidate = hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, iters)
    return hmac.compare_digest(candidate, expected)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("authenticated"):
            flash("You must be logged in to view that page.")
            return redirect(url_for("Login"))
        return f(*args, **kwargs)
    return decorated
