# config.py
from pathlib import Path

# This always pinpoints the directory where config.py lives
BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "real_estate.db"