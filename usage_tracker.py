import json
import os
from pathlib import Path

DB_FILE = Path("usage_db.json")
MAX_QUOTA = 3

def load_db() -> dict:
    if not DB_FILE.exists():
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_db(data: dict):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_usage(username: str) -> int:
    """Retourne le nombre de recherches effectuées par un utilisateur."""
    db = load_db()
    return db.get(username, 0)

def increment_usage(username: str):
    """Incrémente le compteur d'utilisation d'un utilisateur."""
    db = load_db()
    current = db.get(username, 0)
    db[username] = current + 1
    save_db(db)

def has_exceeded_quota(username: str) -> bool:
    """Vérifie si l'utilisateur a dépassé son quota de requêtes."""
    return get_usage(username) >= MAX_QUOTA
